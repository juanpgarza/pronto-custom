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
        string="Transf. Pendientes 2", compute="_compute_transfers_2"
    )

    cancel_in_pending_count = fields.Integer(
        string="Cancelaciones Pendientes", compute="_compute_cancel"
    )

    current_session_id_state = fields.Char("Estado", compute='_compute_current_session_id_state', store=True)

    current_session_user = fields.Char("Usuario", compute='_compute_current_session_user')

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

    def _compute_cancel(self):
        for rec in self:
            cancelaciones_pendientes = self.env['account.cashbox.cancel'].search([('state','in',['new','pending']), ('cancel_cashbox_id', '=', rec.id), '|',('cancel_cashbox_id', '=', rec.id),('cancel_cashbox_id', '=', False)])
            rec.cancel_in_pending_count = len(cancelaciones_pendientes)

    def _compute_current_session_user(self):
        for rec in self:
            if rec.current_session_id.user_ids:
                rec.current_session_user = rec.current_session_id.user_ids[0].name
            else:
                rec.current_session_user = ""

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
