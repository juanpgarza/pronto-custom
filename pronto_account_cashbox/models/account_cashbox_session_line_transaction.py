from odoo import models, fields, api
# from odoo.exceptions import ValidationError

class AccountCashboxSessionLineTransaction(models.Model):
    _name = 'account.cashbox.session.line.transaction'
    _description = 'Movimiento de efectivo'
    _rec_name = 'journal_id'

    # state = fields.Selection([
    #     ('posted', 'Publicado'),
    #     ('cancelled', 'Cancelado'),
    # ], string='Estado', default='posted', required=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('posted', 'Publicado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', compute="_compute_state", store=True)

    name = fields.Char('Descripción')

    session_line_id = fields.Many2one("account.cashbox.session.line", string="Línea de sesión")

    cashbox_session_id = fields.Many2one(
        # 'account.cashbox.session', 
        # string='',
        related='session_line_id.cashbox_session_id',
        )

    cashbox_id = fields.Many2one(
        related='cashbox_session_id.cashbox_id',
        # store=True,
    )

    journal_id = fields.Many2one(
        # 'account.journal', 
        # string='',
        related='session_line_id.journal_id',
        store=True, # para poder agrupar por este campo
        )
    
    transaction_type = fields.Selection([
        ('outbound', 'Egreso'),
        ('inbound', 'Ingreso'),
    ], string='Ingreso/Egreso', default='outbound', required=True)

    transaction_reason = fields.Many2one('account.cashbox.payment.reason', string="Motivo Transacción")

    currency_id = fields.Many2one(
        related='session_line_id.currency_id',
        )

    # amount = fields.Monetary(currency_field='currency_id', compute='_compute_amount')
    amount = fields.Monetary(currency_field='currency_id')
    amount_signed = fields.Monetary(string="Importe",
                                    currency_field='currency_id', 
                                    compute='_compute_amount_signed',
                                    store=True, # para que muestre el total en la vista lista
                                    )

    payment_id = fields.Many2one('account.payment', string="Pago")

    account_id = fields.Many2one('account.account', string="Cuenta contable")

    move_id = fields.Many2one('account.move', string="Asiento contable")


    @api.depends('amount', 'transaction_type')
    def _compute_amount_signed(self):
        for transaction in self:
            if transaction.transaction_type == 'outbound':
                transaction.amount_signed = -transaction.amount
            else:
                transaction.amount_signed = transaction.amount

    @api.model
    def _create_from_payment(self,payment_id,reason_id = False):
        
        vals = {
            'session_line_id': payment_id.cashbox_session_id.line_ids.filtered(lambda x: x.journal_id == payment_id.journal_id).id,
            'transaction_type': 'inbound' if payment_id.payment_type == 'inbound' else 'outbound',
            # 'transaction_reason': reason_id.id,
            'amount': payment_id.amount,
            'payment_id': payment_id.id,
        }

        self.env['account.cashbox.session.line.transaction'].create(vals)

    @api.depends('payment_id.state', 'move_id.state')
    def _compute_state(self):
        for transaction in self:
            if transaction.payment_id:
                # es un pago
                transaction.state = transaction.payment_id.state
            else:
                # es un asiento
                transaction.state = transaction.move_id.state