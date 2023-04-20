from odoo import models, fields
from odoo.exceptions import ValidationError

class AccountCashboxPaymentReason(models.Model):
    _name = 'account.cashbox.payment.reason'
    _description = 'Motivo de movimiento de efectivo'
    
    name = fields.Char('Descripción')

    in_reason = fields.Boolean('Motivo ingreso')

    out_reason = fields.Boolean('Motivo egreso')
