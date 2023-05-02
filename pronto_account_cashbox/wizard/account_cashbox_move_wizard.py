from odoo import models, fields, api, _
from odoo.exceptions import UserError

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

    name = fields.Char(string='Descripción')
    amount = fields.Monetary(string='Importe', currency_field='currency_id', required=True)

    # reason_id = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo', domain="[('id','in',session_cash_control_journal_ids)]")

    # currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.journal_id.currency_id)
    currency_id = fields.Many2one('res.currency', compute="_compute_curency")
    # product_id = fields.Many2one('product.product', string='Producto/Servicio', domain=[('can_be_expensed', '=', True)])

    # adjunto = fields.Binary("Comprobante")
    # file_name = fields.Char("File Name")

    reason_id_in = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo del Ingreso', domain="[('in_reason','=', True)]")
    reason_id_out = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo de Egreso', domain="[('out_reason','=', True)]")

    adjunto = fields.Binary("Comprobante")
    file_name = fields.Char("File Name")

    # def _compute_reason_id(self):
    #     if self.transaction_type == '':
    #         self.
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
            line_ids = [(0, 0, {'debit': self.amount,      'credit': 0.0,      'account_id': reason_id.account_id.id}),
                        (0, 0, {'debit': 0.0,       'credit': self.amount,    'account_id': self.journal_id.default_account_id.id}),]
            
        else:
            reason_id = self.reason_id_in
            line_ids = [(0, 0, {'debit': self.amount,      'credit': 0.0,      'account_id': self.journal_id.default_account_id.id}),
                        (0, 0, {'debit': 0.0,       'credit': self.amount,    'account_id': reason_id.account_id.id}),]
            
        # Registro el asiento contable
        move_id = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': 3,
            # 'date': fields.Date.from_string('2019-01-01'),
            # 'line_ids': [(0, 0, {'debit': self.amount,      'credit': 0.0,      'account_id': reason_id.account_id.id}),(0, 0, {'debit': 0.0,       'credit': self.amount,    'account_id': self.journal_id.default_account_id.id}),],
            'line_ids': line_ids
        })
        move_id.action_post()

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
                'datas_fname': nombre_adjunto,
                'description': nombre_adjunto,
                'res_model': "account.cashbox.session",
                'res_id': self.cashbox_session_id.id,
            }
            new_attachment2 = IrAttachment.create(data_attach2)
