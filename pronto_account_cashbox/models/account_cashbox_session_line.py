from odoo import models, fields
from odoo.exceptions import ValidationError

class AccountCashboxSessionLine(models.Model):
    _inherit = 'account.cashbox.session.line'

    payment_ids = fields.One2many('account.payment', compute='_compute_payment_ids')

    def _compute_payment_ids(self):
        for rec in self:
            rec.payment_ids = rec.cashbox_session_id.payment_ids.filtered(lambda x: x.journal_id.id == rec.journal_id.id)        
