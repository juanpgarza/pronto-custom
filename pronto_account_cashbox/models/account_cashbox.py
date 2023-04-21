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

    def toggle_active(self):
        # Agregar validaciones!!
        # if self.filtered(lambda so: so.state not in ["done", "cancel"] and so.active):
        #     raise UserError(_("Only 'Locked' or 'Canceled' orders can be archived"))
        return super().toggle_active()

    @api.depends("transfer_in_pending_ids")
    def _compute_transfers(self):
        for session in self:
            session.transfer_in_pending_count = len(session.transfer_in_pending_ids)