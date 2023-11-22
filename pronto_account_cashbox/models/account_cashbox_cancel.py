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

    cancel_cashbox_id = fields.Many2one(
        'account.cashbox', 
        string='Caja objetivo cancelación',
        related='cancel_payment_group_id.cashbox_id',
        )

    cancel_cashbox_session_id = fields.Many2one(
        'account.cashbox.session',
        string='Sesión objetivo cancelación',
        related='cancel_payment_group_id.cashbox_session_id',
    )

    ccs_id = fields.Integer(related='cancel_cashbox_session_id.id')

    cancel_payment_group_id = fields.Many2one(
        comodel_name='account.payment.group',
        string="Pago cancelado", copy=False)

    cancel_reason_note = fields.Char(
        related='cancel_payment_group_id.cancel_reason_note',
    )

    partner_id = fields.Many2one('res.partner', string="Cliente/Proveedor", related='cancel_payment_group_id.partner_id',)

    currency_id = fields.Many2one(
        'res.currency',
        related='cancel_payment_group_id.currency_id',)

    cancel_payments_amount = fields.Monetary(
        string='Monto cancelado',
        related='cancel_payment_group_id.payments_amount',
    )

    new_payment_group_id = fields.Many2one(
        comodel_name='account.payment.group',
        string="Pago nuevo", copy=False, domain="[('state','=','posted'),('cashbox_session_id','=',cancel_cashbox_session_id)]")
    # ('cashbox_session_id','=',cancel_cashbox_session_id),
    new_payments_amount = fields.Monetary(
        string='Monto pago nuevo',
        related='new_payment_group_id.payments_amount',
    )

    matched_move_line_ids = fields.Many2many('account.move.line',
                                             string='Comprobantes imputados del recibo cancelado')
    
    def action_enviar(self):
        for rec in self:
            rec.write({'state': 'pending',})

    def action_aprobar(self):
        for rec in self:
            rec.write({'state': 'approved',})