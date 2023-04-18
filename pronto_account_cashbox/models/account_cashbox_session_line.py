from odoo import models, fields
from odoo.exceptions import ValidationError

class AccountCashboxSessionLine(models.Model):
    _inherit = 'account.cashbox.session.line'

    payment_ids = fields.One2many('account.payment', compute='_compute_payment_ids')

    def _compute_payment_ids(self):
        for rec in self:
            rec.payment_ids = rec.cashbox_session_id.payment_ids.filtered(lambda x: x.journal_id.id == rec.journal_id.id)        

    def write(self, values):
        for rec in self:
             if 'balance_start' in values and values['balance_start'] != rec.balance_start:
                    raise ValidationError(
                            'El saldo inicial informado no coincide con el saldo final de la última sesión.'
                            )
        res = super(AccountCashboxSessionLine, self).write(values)

        return res