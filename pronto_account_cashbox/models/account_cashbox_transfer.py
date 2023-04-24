from odoo import models, fields
from odoo.exceptions import ValidationError

TRANSFER_STATE = [
    ('draft', 'Borrador'),
    ('sent', 'Enviada'),
    ('received', 'Recibida'),
]

class AccountCashboxTransfer(models.Model):
    _name = 'account.cashbox.transfer'
    _description = 'Transferencia entre cajas'
    _rec_name = 'name'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(related='origin_payment_id.name', string="Número")

    state = fields.Selection(
        TRANSFER_STATE, required=True, readonly=False,
        index=True, copy=False, default='draft', string="Estado")

    # origin_cashbox_id = fields.Many2one('account.cashbox', required=True, states={'draft': [('readonly', False)]}, readonly=True)
    origin_cashbox_id = fields.Many2one(
        'account.cashbox', 
        string='Caja Origen',
        related='origin_payment_id.cashbox_id',
        )

    origin_cashbox_session_id = fields.Many2one(
        'account.cashbox.session',
        string='Sesión Origen',
        related='origin_payment_id.cashbox_session_id',
    )

    amount = fields.Monetary('Importe', related='origin_payment_id.amount',)
    currency_id = fields.Many2one('res.currency', related='origin_payment_id.currency_id',)

    # origin_cashbox_id y origin_cashbox_session_id debería ser related de este!!
    # amount y currency_id tambien?!?!?!
    origin_payment_id = fields.Many2one(
        comodel_name='account.payment',
        string="Pago origen", copy=False)

    destination_cashbox_id = fields.Many2one('account.cashbox', string='Caja Destino', required=True, readonly=True)

    destination_payment_id = fields.Many2one(
        comodel_name='account.payment',
        string="Pago destino", copy=False)

    destination_cashbox_session_id = fields.Many2one(
        'account.cashbox.session',
        string='Sesión Destino',
        related='destination_payment_id.cashbox_session_id',
    )