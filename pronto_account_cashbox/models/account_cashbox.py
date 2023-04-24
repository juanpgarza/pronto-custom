from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountCashbox(models.Model):
    _inherit = 'account.cashbox'

    active = fields.Boolean(default=True)

    transfer_in_pending_ids = fields.One2many(
            'account.cashbox.transfer', 
            'destination_cashbox_id',
            domain=lambda self: [('state','=','sent'), ('destination_cashbox_id', '=', self.id)],
            store=True,
            )
    transfer_in_pending_count = fields.Integer(
        string="Transf. Pendientes", compute="_compute_transfers"
    )

    transfer_in_pending_count_2 = fields.Integer(
        string="Transf. Pendientes", compute="_compute_transfers_2"
    )

    current_session_id_state = fields.Char("Estado", compute='_compute_current_session_id_state', store=True)

    def toggle_active(self):
        # Agregar validaciones!!
        # if self.filtered(lambda so: so.state not in ["done", "cancel"] and so.active):
        #     raise UserError(_("Only 'Locked' or 'Canceled' orders can be archived"))
        return super().toggle_active()

    @api.depends("transfer_in_pending_ids")
    def _compute_transfers(self):
        for session in self:
            session.transfer_in_pending_count = len(session.transfer_in_pending_ids)

    # @api.depends("transfer_in_pending_ids")
    def _compute_transfers_2(self):
        for rec in self:
            transferencias_pendientes = self.env['account.cashbox.transfer'].search([('state','=','sent'), ('destination_cashbox_id', '=', rec.id)])
            rec.transfer_in_pending_count_2 = len(transferencias_pendientes)

    @api.depends("current_session_id","current_session_id.state")
    def _compute_current_session_id_state(self):
        for rec in self:
            estado = ''
            if rec.current_session_id:
                if rec.current_session_id.state == 'draft':
                    estado = 'Borrador'
                elif rec.current_session_id.state == 'opened':
                    estado = 'Abierto'
                elif rec.current_session_id.state == 'closing_control':
                    estado = 'Control de Cierre'
                else:
                    estado = 'CERRADA'
            else:
                estado = 'CERRADA'
            
            rec.current_session_id_state = estado
