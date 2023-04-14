from odoo import models, fields
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    cashbox_id = fields.Many2one(
        related='cashbox_session_id.cashbox_id',
        store=True,
    )

