from odoo import models, fields
from odoo.exceptions import ValidationError

CANCEL_STATE = [
    ('new', 'Nueva'),
    ('pending', 'Enviada'),
    ('approved', 'Aprobada'),
]


class AccountCashboxCancel(models.Model):
    _name = 'account.cashbox.cancel'
    _description = 'Cancelación'
    _rec_name = 'cancel_payment_group_id'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # name = fields.Char(related='cancel_payment_group_id.name', string="Número")

    state = fields.Selection(
        CANCEL_STATE, required=True, readonly=False,
        index=True, copy=False, default='new', string="Estado")

    # origin_cashbox_id = fields.Many2one('account.cashbox', required=True, states={'draft': [('readonly', False)]}, readonly=True)
    origin_cashbox_id = fields.Many2one(
        'account.cashbox', 
        string='Caja objetivo cancelación',
        related='cancel_payment_group_id.cashbox_id',
        )

    origin_cashbox_session_id = fields.Many2one(
        'account.cashbox.session',
        string='Sesión objetivo cancelación',
        related='cancel_payment_group_id.cashbox_session_id',
    )

    # amount = fields.Monetary('Importe', related='origin_payment_id.amount',)
    # currency_id = fields.Many2one('res.currency', related='origin_payment_id.currency_id',)

    cancel_payment_group_id = fields.Many2one(
        comodel_name='account.payment.group',
        string="Pago cancelado", copy=False)

    new_payment_group_id = fields.Many2one(
        comodel_name='account.payment.group',
        string="Pago nuevo", copy=False, domain="[('cashbox_session_id','=',origin_cashbox_session_id),('state','!=','cancel')]")
    

