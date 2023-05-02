from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountCashboxSessionLine(models.Model):
    _inherit = 'account.cashbox.session.line'

    payment_ids = fields.One2many('account.payment', compute='_compute_payment_ids')

    transaction_ids = fields.One2many('account.cashbox.session.line.transaction', 'session_line_id')

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

    # este lo tengo que sobre-escribir para tomar transaction (payment + account moves) en lugar de solo payments
    @api.depends('cashbox_session_id.payment_ids','cashbox_session_id.payment_ids.state', 'balance_start','transaction_ids','transaction_ids.state')
    def _compute_amounts(self):
        # import pdb; pdb.set_trace()
        payments_lines = self.env['account.cashbox.session.line.transaction'].search([
                ('cashbox_session_id', 'in', self.mapped('cashbox_session_id').ids), ('state', '=', 'posted')])
        for record in self:
            amount = sum(payments_lines.filtered(
                lambda p: p.cashbox_session_id == record.cashbox_session_id and p.journal_id == record.journal_id
                ).mapped('amount_signed'))
            record.amount = amount
            record.balance_end = amount + record.balance_start
            self -= record
        self.amount = False
        self.balance_end = False