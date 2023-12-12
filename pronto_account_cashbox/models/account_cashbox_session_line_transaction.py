from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountCashboxSessionLineTransaction(models.Model):
    _name = 'account.cashbox.session.line.transaction'
    _description = 'Movimiento de efectivo'
    _rec_name = 'journal_id'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'id'

    # state = fields.Selection([
    #     ('posted', 'Publicado'),
    #     ('cancelled', 'Cancelado'),
    # ], string='Estado', default='posted', required=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('posted', 'Publicado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', compute="_compute_state", store=True)

    # name = fields.Char('Descripción')
    
    ref = fields.Char(
                string='Referencia',
                compute='_compute_ref',
                store=True,)
    
    session_line_id = fields.Many2one("account.cashbox.session.line", string="Línea de sesión")

    cashbox_session_id = fields.Many2one(
        # 'account.cashbox.session', 
        # string='',
        related='session_line_id.cashbox_session_id',
        store=True,
        )

    cashbox_id = fields.Many2one(
        related='cashbox_session_id.cashbox_id',
        store=True,
    )

    partner_id = fields.Many2one('res.partner',
                                 string="Socio",
                                 compute="_compute_transaction_group",
                                 store=True,)

    journal_id = fields.Many2one(
        # 'account.journal', 
        string='Diario',
        related='session_line_id.journal_id',
        store=True, # para poder agrupar por este campo
        )
    
    transaction_type = fields.Selection([
        ('outbound', 'Egreso'),
        ('inbound', 'Ingreso'),
    ], string='Ingreso/Egreso', default='outbound', required=True)

    transaction_reason = fields.Many2one('account.cashbox.payment.reason', string="Motivo Transacción")

    transaction_group = fields.Selection([
                        ('recibo', 'Recibo'),
                        ('orden_pago', 'Orden de Pago'),
                        # ('factura_proveedor', 'Factura de compra'),
                        ('asiento_contable_directo', 'Asiento Directo'),
                        ('operacion_bancaria', 'Extracción/Depósito Bancario'),
                        ('transferencia_entre_cajas', 'Transferencia entre cajas'),
                    ], 
                    string='Grupo de transacción',
                    compute="_compute_transaction_group",
                    store=True,
                    # required=True,
                    )

    transaction_group_detail = fields.Char(string="Detalle",
                                           compute="_compute_transaction_group",
                                            store=True,)

    currency_id = fields.Many2one(
        related='session_line_id.currency_id',
        )

    amount = fields.Monetary(string="Importe", 
                             currency_field='currency_id', 
                             compute='_compute_amount',
                             store=True,)

    # amount = fields.Monetary(string="Importe",
    #                          currency_field='currency_id')
    amount_signed = fields.Monetary(string="Importe (con signo)",
                                    currency_field='currency_id', 
                                    compute='_compute_amount_signed',
                                    store=True, # para que muestre el total en la vista lista
                                    )

    payment_id = fields.Many2one('account.payment', string="Pago")

    account_id = fields.Many2one('account.account', string="Cuenta contable")

    move_id = fields.Many2one('account.move', string="Asiento contable")

    @api.depends('payment_id.amount', 'move_id.amount_total')
    def _compute_amount(self):
        # Por ahora solo en asientos directos y factura de prov
        for transaction in self:
            if transaction.payment_id:
                transaction.amount = transaction.payment_id.amount
            else:
                transaction.amount = transaction.move_id.amount_total

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
    
    @api.depends('payment_id', 'move_id')
    def _compute_transaction_group(self):
        for transaction in self:
            if transaction.payment_id:
            # es un pago. y puede ser:
            # Todo menos un 'asiento_contable_directo'
                if transaction.payment_id.payment_group_id:                
                    transaction.partner_id = transaction.payment_id.payment_group_id.partner_id
                    if transaction.transaction_type == 'inbound':
                    # tiene un payment group y es inbound
                        transaction.transaction_group = 'recibo'
                        transaction.transaction_group_detail = 'Cobro a cliente'
                    else:
                    # tiene un payment group y es outbound
                        transaction.transaction_group = 'orden_pago'
                        transaction.transaction_group_detail = 'Pago a proveedor'
                else:
                    # son movimientos internos usando payments
                    # y pueden ser: 
                    # . movimientos entre cajas (entre diarios de efectivo)
                    # . operaciones bancarias (entre un diario de efectivo y uno de banco)
                    transaction.partner_id = False
                    if transaction.payment_id.cashbox_transfer_id:
                    # es una transferencia entre cajas
                        transaction.transaction_group = 'transferencia_entre_cajas'
                        cashbox_id = transaction.payment_id.cashbox_transfer_id.destination_cashbox_id
                        if transaction.transaction_type == 'inbound':
                            transaction.transaction_group_detail = 'Recepción desde caja {}'.format(cashbox_id.name)
                        else:
                            transaction.transaction_group_detail = 'Envío a caja {}'.format(cashbox_id.name)
                    else:
                    # es una operación bancaria
                        transaction.transaction_group = 'operacion_bancaria'
                        journal_id = transaction.payment_id.destination_journal_id
                        if transaction.journal_id in transaction.cashbox_session_id.session_cash_control_journal_ids:                            
                            if transaction.transaction_type == 'outbound':
                                detail = 'Depósito en {}'.format(journal_id.name)
                            else:
                                detail = 'Extracción de {}'.format(journal_id.name)
                        else:
                            if transaction.transaction_type == 'outbound':
                                detail = 'Extracción a {}'.format(journal_id.name)
                            else:
                                detail = 'Depósito desde {}'.format(journal_id.name)
                        
                        transaction.transaction_group_detail = detail

            else:
                if transaction.move_id:
                    if transaction.move_id.move_type == 'entry':
                        transaction.transaction_group = 'asiento_contable_directo'
                        transaction.partner_id = False
                        transaction.transaction_group_detail = transaction.transaction_reason.name
                    # else:
                    #     if transaction.move_id.move_type == 'in_invoice':
                    #         transaction.transaction_group = 'factura_proveedor'
                    #         transaction.partner_id = transaction.move_id.partner_id
                    #         transaction.transaction_group_detail = 'Factura de compra de {}'.format(transaction.partner_id.name)
                else:
                    raise ValidationError("Transacción sin clasificar!!")

    @api.depends('payment_id.ref', 'move_id.ref')
    def _compute_ref(self):
        # Por ahora solo en asientos directos y factura de prov
        for transaction in self:
            # if transaction.transaction_group in ('asiento_contable_directo','factura_proveedor'):
            #     transaction.ref = transaction.move_id.ref
            # else:
            #     transaction.ref = False

            if transaction.move_id:
                transaction.ref = transaction.move_id.ref
            elif transaction.payment_id:
                pago = transaction.payment_id
                if pago.payment_method_line_id.code == 'new_third_party_checks' and pago.l10n_latam_check_bank_id and pago.l10n_latam_check_payment_date: 
                    transaction.ref = "{} - {}".format(pago.l10n_latam_check_bank_id.name,pago.l10n_latam_check_payment_date.strftime("%d/%m/%Y"))
                else:
                    transaction.ref = transaction.payment_id.ref
            else:
                transaction.ref = False