from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class AccountCashboxMoveWizard(models.TransientModel):
    _name = 'account.cashbox.move.wizard'
    _description = 'Operaciones varias'

    # tipo_de_movimiento = fields.Selection([('recibo', 'Recibo'),
    #      ('pago', 'Pago'),
    #      ('gasto', 'Gasto')],
    #     string="Tipo de Movimiento",)

    transaction_type = fields.Selection([
        ('outbound', 'Egreso'),
        ('inbound', 'Ingreso'),
    ], string='Ingreso/Egreso', default='outbound', required=True)

    cashbox_session_id = fields.Many2one('account.cashbox.session', string='Session')
    session_cash_control_journal_ids = fields.Many2many('account.journal', related='cashbox_session_id.session_cash_control_journal_ids')
    
    def _default_journal_id(self):
        # que siempre ponga por default un diario en ARS
        # los diarios que no tienen informada la moneda son en ARS
        diario_efectivo_ars = self.env['account.cashbox.session'].browse(self._context.get('active_id', False)).session_cash_control_journal_ids.filtered(lambda x: not x.currency_id)
        # import pdb; pdb.set_trace()
        if diario_efectivo_ars:
            return diario_efectivo_ars[0]
        else:
            return False

    journal_id = fields.Many2one('account.journal',string='Diario',domain="[('id','in',session_cash_control_journal_ids)]",default=_default_journal_id)

    amount = fields.Monetary(string='Importe', currency_field='currency_id', required=True)

    company_id = fields.Many2one(
        related="journal_id.company_id", readonly=True
    )

    company_currency_id = fields.Many2one(
        related="company_id.currency_id", readonly=True
    )

    amount_company_currency = fields.Monetary(
        string='Amount on Company Currency',
        compute='_compute_amount_company_currency',
        inverse='_inverse_amount_company_currency',
        currency_field='company_currency_id',
    )

    other_currency = fields.Boolean(
        compute='_compute_other_currency',
    )
    force_amount_company_currency = fields.Monetary(
        string='Forced Amount on Company Currency',
        currency_field='company_currency_id',
        copy=False,
    )

    exchange_rate = fields.Float(
        string='Exchange Rate',
        compute='_compute_exchange_rate',
        # readonly=False,
        # inverse='_inverse_exchange_rate',
        digits=(16, 4),
    )
    
    # reason_id = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo', domain="[('id','in',session_cash_control_journal_ids)]")

    # currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.journal_id.currency_id)
    currency_id = fields.Many2one('res.currency')
    # product_id = fields.Many2one('product.product', string='Producto/Servicio', domain=[('can_be_expensed', '=', True)])

    # adjunto = fields.Binary("Comprobante")
    # file_name = fields.Char("File Name")

    reason_id_in = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo del Ingreso', domain="[('in_reason','=', True)]")
    reason_id_out = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo de Egreso', domain="[('out_reason','=', True)]")

    adjunto = fields.Binary("Comprobante")
    file_name = fields.Char("File Name")

    ref = fields.Char(string='Referencia')

    en_clima = fields.Boolean("En clima")

    # def _compute_reason_id(self):
    #     if self.transaction_type == '':
    #         self.

    @api.depends('amount', 'other_currency', 'amount_company_currency')
    def _compute_exchange_rate(self):
        for rec in self:
            if rec.other_currency:
                rec.exchange_rate = rec.amount and (
                    rec.amount_company_currency / rec.amount) or 0.0
            else:
                rec.exchange_rate = False

    @api.depends('amount', 'other_currency', 'force_amount_company_currency')
    def _compute_amount_company_currency(self):
        """
        * Si las monedas son iguales devuelve 1
        * si no, si hay force_amount_company_currency, devuelve ese valor
        * sino, devuelve el amount convertido a la moneda de la cia
        """
        for rec in self:
            if not rec.other_currency:
                amount_company_currency = rec.amount
            elif rec.force_amount_company_currency:
                amount_company_currency = rec.force_amount_company_currency
            else:
                amount_company_currency = rec.currency_id._convert(
                    rec.amount, rec.company_id.currency_id,
                    rec.company_id, datetime.today())
            rec.amount_company_currency = amount_company_currency

    # this onchange is necesary because odoo, sometimes, re-compute
    # and overwrites amount_company_currency. That happends due to an issue
    # with rounding of amount field (amount field is not change but due to
    # rouding odoo believes amount has changed)
    @api.onchange('amount_company_currency')
    def _inverse_amount_company_currency(self):
        for rec in self:
            if rec.other_currency and rec.amount_company_currency != \
                    rec.currency_id._convert(
                        rec.amount, rec.company_id.currency_id,
                        rec.company_id, datetime.today()):
                force_amount_company_currency = rec.amount_company_currency
            else:
                force_amount_company_currency = False
            rec.force_amount_company_currency = force_amount_company_currency

    @api.depends('currency_id')
    def _compute_other_currency(self):
        for rec in self:
            rec.other_currency = False
            if rec.company_currency_id and rec.currency_id and \
               rec.company_currency_id != rec.currency_id:
                rec.other_currency = True

    @api.onchange('reason_id_in', 'reason_id_in')
    def _onchange_price_total(self):
        if self.transaction_type == 'outbound':
            self.en_clima = self.reason_id_out.en_clima
        else:
            self.en_clima = self.reason_id_in.en_clima

    @api.depends('journal_id')
    def _compute_curency(self):
        for rec in self:
            rec.currency_id = rec.journal_id.currency_id or rec.journal_id.company_id.currency_id

    @api.model
    def default_get(self, field_names):
        defaults = super(AccountCashboxMoveWizard, self).default_get(field_names)
        defaults['cashbox_session_id'] = self.env.context['active_id']
        # defaults['tipo_de_movimiento'] = self.env.context['tipo_de_movimiento']
        return defaults

    def do_cash_out(self):

        if self.amount == 0:
            raise UserError('El importe no puede ser cero.')

        if self.transaction_type == 'outbound':
            reason_id = self.reason_id_out
            line_ids = [(0, 0, {'debit': self.amount_company_currency,      'credit': 0.0, 'currency_id': self.currency_id.id, 'amount_currency': self.amount,      'account_id': reason_id.account_id.id}),
                        (0, 0, {'debit': 0.0,       'credit': self.amount_company_currency, 'currency_id': self.currency_id.id, 'amount_currency': self.amount * -1,    'account_id': self.journal_id.default_account_id.id}),]
            
        else:
            reason_id = self.reason_id_in
            line_ids = [(0, 0, {'debit': self.amount_company_currency,      'credit': 0.0, 'currency_id': self.currency_id.id, 'amount_currency': self.amount,      'account_id': self.journal_id.default_account_id.id}),
                        (0, 0, {'debit': 0.0,       'credit': self.amount_company_currency, 'currency_id': self.currency_id.id, 'amount_currency': self.amount * -1,    'account_id': reason_id.account_id.id}),]
            
        # Registro el asiento contable
        move_id = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': self.journal_id.id,
            # 'date': fields.Date.from_string('2019-01-01'),
            # 'line_ids': [(0, 0, {'debit': self.amount,      'credit': 0.0,      'account_id': reason_id.account_id.id}),(0, 0, {'debit': 0.0,       'credit': self.amount,    'account_id': self.journal_id.default_account_id.id}),],
            'line_ids': line_ids,
            'ref': self.ref,
        })
        move_id.action_post()

        clima_enable = 'en_clima' in self.env['account.move']._fields
        if clima_enable:
            move_id.en_clima = self.en_clima

        # Registro la transacción
        vals = {
            'session_line_id': self.cashbox_session_id.line_ids.filtered(lambda x: x.journal_id == self.journal_id).id,
            'transaction_type': self.transaction_type,
            'transaction_reason': reason_id.id,
            'amount': self.amount,
            'account_id': reason_id.account_id.id,
            'move_id': move_id.id,
        }

        self.env['account.cashbox.session.line.transaction'].create(vals)

        if self.adjunto:
            nombre_adjunto = self.file_name
            IrAttachment = self.env['ir.attachment']

            data_attach2 = {
                'name': nombre_adjunto,
                'datas': self.adjunto,
                'type': 'binary',
                'description': nombre_adjunto,
                'res_model': "account.cashbox.session",
                'res_id': self.cashbox_session_id.id,
            }
            new_attachment2 = IrAttachment.create(data_attach2)

    @api.onchange('journal_id')
    def _onchange_journal(self):
        # if self.journal_id and self.journal_id.currency_id:
        # import pdb; pdb.set_trace()
        self.currency_id = self.journal_id.currency_id or self.journal_id.company_id.currency_id
        # if self.journal_id and self.journal_id.currency_id:
        #     new_currency = self.journal_id.currency_id
        #     if new_currency != self.currency_id:
        #         self.currency_id = new_currency
        #         self._onchange_currency()
        # if self.state == 'draft' and self._get_last_sequence(lock=False) and self.name and self.name != '/':
        #     self.name = '/'