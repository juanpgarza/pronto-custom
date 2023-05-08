from odoo import models, fields
from odoo.exceptions import ValidationError

class AccountCashboxPaymentReason(models.Model):
    _name = 'account.cashbox.payment.reason'
    _description = 'Motivo de movimiento de efectivo'

    active = fields.Boolean(default=True)

    name = fields.Char('Descripción')

    in_reason = fields.Boolean('Motivo ingreso')

    out_reason = fields.Boolean('Motivo egreso')

    account_id = fields.Many2one('account.account', string="Cuenta contable")

    en_clima = fields.Boolean("En clima")