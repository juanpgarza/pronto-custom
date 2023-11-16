from odoo import models, fields, api


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    cancel_reason_note = fields.Char("Detalle el motivo de la cancelación",tracking=True)

    cashbox_session_id = fields.Many2one(
                                'account.cashbox.session',
                                string="Sesión de caja",
                                compute="_compute_cashbox_session_id",
                                store=True,)
    
    cashbox_id = fields.Many2one(
        related='cashbox_session_id.cashbox_id',
        store=True,
    )

    @api.depends("payment_ids.cashbox_session_id")
    def _compute_cashbox_session_id(self):
        for rec in self:
            if rec.payment_ids:
                rec.cashbox_session_id = rec.payment_ids[0].cashbox_session_id
            else:
                rec.cashbox_session_id = False
