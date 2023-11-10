from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class AccountCashboxSupllierBillWizard(models.TransientModel):
    _name = 'account.cashbox.supplier.bill.wizard'
    _description = 'Factura de compra'

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

    def _default_purchase_journal_id(self):
        purchase_journal_ids = self.env['account.journal'].search([('type','=','purchase')])
        if purchase_journal_ids:
            return purchase_journal_ids[0]
        else:
            return False

    journal_id = fields.Many2one('account.journal',string='Diario',domain="[('id','in',session_cash_control_journal_ids)]",default=_default_journal_id)
    purchase_journal_id = fields.Many2one(
                                    'account.journal',
                                    string='Diario de Compra',
                                    domain="[]",
                                    default=_default_purchase_journal_id
                                    )
    
    l10n_latam_available_document_type_ids = fields.Many2many(comodel_name='l10n_latam.document.type', compute='_compute_l10n_latam_available_document_types')    
    
    invoice_date = fields.Date(string='Fecha Factura', default=fields.Date.context_today)

    partner_id = fields.Many2one('res.partner', 
                                 string="Proveedor",
                                 domain=[('is_supplier', '=', True)],
                                 )

    l10n_latam_document_type_id = fields.Many2one(
                            'l10n_latam.document.type', 
                            string='Tipo de Documento',
                            domain="[('id','in',l10n_latam_available_document_type_ids)]",
                            )

    l10n_latam_document_number = fields.Char('Número de Documento')

    product_id = fields.Many2one('product.product', 
                                string='Producto/Concepto', 
                                domain=[('can_be_expensed', '=', True)],
                                )

    price_unit = fields.Float(string='Precio Neto (Sin IVA)')

    price_total = fields.Monetary(string='Precio Total', 
                                # readonly=True,
                                currency_field='currency_id')

    currency_id = fields.Many2one('res.currency', compute="_compute_curency")

    adjunto = fields.Binary("Comprobante")
    file_name = fields.Char("File Name")

    ref = fields.Char(string='Referencia')

    @api.depends('purchase_journal_id', 'partner_id')
    def _compute_l10n_latam_available_document_types(self):
        self.l10n_latam_available_document_type_ids = False
        self.l10n_latam_document_type_id = False
        if self.purchase_journal_id and self.partner_id:
            if self.purchase_journal_id.l10n_latam_use_documents and not self.partner_id.l10n_ar_afip_responsibility_type_id:
                raise ValidationError('El proveedor {} no tiene informada la Responsabilidad AFIP'.format(self.partner_id.name))
                
            domain = [
                ('internal_type', '=', 'invoice' ), 
                ('country_id', '=', self.purchase_journal_id.company_id.account_fiscal_country_id.id),
                ('l10n_ar_letter', 'in', self.purchase_journal_id._get_journal_letter(counterpart_partner= self.partner_id) ),
            ]
            self.l10n_latam_available_document_type_ids = self.env['l10n_latam.document.type'].search(domain)
            if self.l10n_latam_available_document_type_ids:
                self.l10n_latam_document_type_id = self.l10n_latam_available_document_type_ids[0]

    # src/addons/l10n_ar/models/account_move.py:150
    # esto acá NO ME FUNCIONA!!
    # @api.onchange('purchase_journal_id','partner_id')
    # def _onchange_afip_responsibility(self):
    #     if self.purchase_journal_id.l10n_latam_use_documents and not self.partner_id.l10n_ar_afip_responsibility_type_id:
    #         # raise ValidationError('El proveedor {} no tiene informada la Responsabilidad AFIP'.format(self.partner_id.name))
    #         return {'warning': {
    #             'title': _('Falta informar Responsabilidad AFIP'),
    #             'message': _('Configure la Responsabilidad AFIP de "%s" para poder continuar') % (
    #                 self.partner_id.name)}} 
            
    @api.depends('journal_id')
    def _compute_curency(self):
        for rec in self:
            rec.currency_id = rec.journal_id.currency_id or rec.journal_id.company_id.currency_id

    @api.model
    def default_get(self, field_names):
        defaults = super(AccountCashboxSupllierBillWizard, self).default_get(field_names)
        defaults['cashbox_session_id'] = self.env.context['active_id']
        return defaults

    @api.onchange('price_unit', 'product_id')
    def _onchange_price_total(self):

        if self.price_unit == 0:
            self.price_total = 0
        else:
            AccountMoveLine = self.env['account.move.line']

            res = AccountMoveLine._get_price_total_and_subtotal_model(
                price_unit= self.price_unit,
                quantity= 1,
                discount= 0,
                currency= self.currency_id,
                product= self.product_id,
                partner= self.partner_id,
                taxes=self.product_id.supplier_taxes_id,
                move_type='in_invoice',            
            )

            # import pdb; pdb.set_trace()
            self.price_total = res["price_total"]

    def do_cash_out(self):

        if self.cashbox_session_id.state in ('draft','closed'):
            raise UserError('Debe iniciar sesión de caja para realizar este movimiento.')

        if self.price_unit == 0:
            raise ValidationError('El importe no puede ser cero.')      
        
        move_id = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'invoice_date': self.invoice_date,
            'partner_id': self.partner_id.id,
            'journal_id': self.purchase_journal_id.id,
            'pay_now_journal_id': self.journal_id.id,
            'l10n_latam_document_type_id': self.l10n_latam_document_type_id.id,
            'l10n_latam_document_number': self.l10n_latam_document_number,
            'ref': self.ref,
            # 'invoice_cash_rounding_id': self.cash_rounding_b.id,
            # 'invoice_payment_term_id': self.pay_terms_a.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_id.id,
                    'price_unit': self.price_unit,
                    'tax_ids': [(6, 0, self.product_id.supplier_taxes_id.ids)],
                    'product_uom_id':  self.product_id.uom_id.id,
                }),
            ],
        })
        move_id.action_post()

        # Registro la transacción
        # vals = {
        #     'session_line_id': self.cashbox_session_id.line_ids.filtered(lambda x: x.journal_id == self.journal_id).id,
        #     'transaction_type': 'outbound',
        #     'amount': self.price_total,
        #     'move_id': move_id.id,
        # }

        # self.env['account.cashbox.session.line.transaction'].create(vals)

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
