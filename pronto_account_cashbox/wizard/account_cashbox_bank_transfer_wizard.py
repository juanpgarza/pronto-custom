from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountCashboxBankTransferWizard(models.TransientModel):
    _name = 'account.cashbox.bank.transfer.wizard'
    _description = 'Depósito / Extracción'

    transaction_type = fields.Selection([
        ('outbound', 'Depósito'),
        ('inbound', 'Extracción'),
    ], string='Depósito / Extracción', default='outbound', required=True)

    session_line_id = fields.Many2one("account.cashbox.session.line", string="Línea de sesión")

    cash_journal_id = fields.Many2one('account.journal',string='Diario Efectivo',related='session_line_id.journal_id')

    bank_journal_id = fields.Many2one('account.journal',string='Diario Banco',domain=[('type','=','bank')])

    amount = fields.Monetary(string='Importe', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', compute="_compute_currency")

    @api.depends('cash_journal_id')
    def _compute_currency(self):
        for rec in self:
            rec.currency_id = rec.cash_journal_id.currency_id or rec.cash_journal_id.company_id.currency_id

    @api.model
    def default_get(self, field_names):
        defaults = super(AccountCashboxBankTransferWizard, self).default_get(field_names)
        defaults['session_line_id'] = self.env.context['active_id']
        return defaults

    def do_transfer(self):

        if self.amount == 0:
            raise UserError('El importe no puede ser cero.')

        if self.transaction_type == 'outbound':
            # DEPOSITO
            payment_vals = {
                'amount': self.amount,
                'payment_type': self.transaction_type,
                # 'partner_type': partner_type,
                'journal_id': self.cash_journal_id.id,
                'partner_id': self.cash_journal_id.company_id.partner_id.id,
                'payment_method_line_id': self.cash_journal_id._get_available_payment_method_lines('outbound').filtered(lambda x: x.code == 'manual').id,
                'cashbox_session_id': self.session_line_id.cashbox_session_id.id,
                'ref': 'Depósito desde Caja',
                'destination_journal_id': self.bank_journal_id.id,
            }
        else:
            # EXTRACCION
            return True
        
        payment = self.env['account.payment'].create(payment_vals)            