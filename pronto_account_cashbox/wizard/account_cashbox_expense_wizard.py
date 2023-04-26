from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountCashboxExpenseWizard(models.TransientModel):
    _name = 'account.cashbox.expense.wizard'
    _description = 'Gasto'

    tipo_de_movimiento = fields.Selection([('recibo', 'Recibo'),
         ('pago', 'Pago'),
         ('gasto', 'Gasto')],
        string="Tipo de Movimiento",)

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
    unit_amount = fields.Float(string='Importe', digits=0, required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.user.company_id.currency_id)
    product_id = fields.Many2one('product.product', string='Producto/Servicio', domain=[('can_be_expensed', '=', True)])

    adjunto = fields.Binary("Comprobante")
    file_name = fields.Char("File Name")

    reason_id_in = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo de movimiento (Ingreso)', domain="[('in_reason','=', True)]")
    reason_id_out = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo de movimiento (Salida)', domain="[('out_reason','=', True)]")

    @api.model
    def default_get(self, field_names):
        defaults = super(AccountCashboxExpenseWizard, self).default_get(field_names)
        defaults['cashbox_session_id'] = self.env.context['active_id']
        defaults['tipo_de_movimiento'] = self.env.context['tipo_de_movimiento']
        return defaults

    def do_cash_out(self):

        if self.unit_amount == 0:
            raise UserError('El importe no puede ser cero.')

        if self.tipo_de_movimiento in ('pago','gasto'):
            partner_id = self.env.ref('pronto_account_cashbox.proveedor_no_habitual')
            payment_type = 'outbound'
            partner_type = 'supplier'
            
        else:
            partner_id = self.env.ref('pronto_account_cashbox.cliente_generico')
            payment_type = 'inbound'
            partner_type = 'customer'

        vals = {
            'partner_id': partner_id.id,
            'amount': self.unit_amount,
            'payment_type': payment_type,
            'partner_type': partner_type,
            'journal_id': self.journal_id.id,
            'payment_method_line_id': self.journal_id._get_available_payment_method_lines('outbound').filtered(lambda x: x.code == 'manual').id,
            'cashbox_session_id': self.cashbox_session_id.id,
            'ref': self.name,
            'reason_id': self.reason_id_in.id or self.reason_id_out.id,
        }
        payment = self.env['account.payment'].create(vals)
        payment.action_post()

        # le cambio el talonario a uno en clima (clima_base.receiptbook_clima_fsm)
        clima_enable = 'en_clima' in self.env['account.move']._fields
        if clima_enable:
            if payment_type == 'inbound':
                payment.payment_group_id.receiptbook_id = self.env.ref('clima_base.receiptbook_clima_fsm')
            payment.payment_group_id.en_clima = True
            # no me alcanza con cambiar el talonario. Tengo que cambiar la marca en el payment group y en el account move
            # esto lo tengo que cambiar!! cuando le saco la marca a un payment, los asientos asociados se debería cambiar automáticamente!!
            payment.payment_group_id.move_line_ids.move_id.write({'en_clima': True})

        if self.tipo_de_movimiento == 'gasto':
            vals0 = {
                'name': self.name,
                'unit_amount' : self.unit_amount,
                'product_id': self.product_id.id,
                'quantity': 1,
                # 'employee_id': self.box_session_id.user_id.employee_ids.id,
                'payment_mode': "company_account",
                'payment_id': payment.id,
            }

            expense_id = self.env['hr.expense'].create(vals0)

        # Adjunto
        if self.adjunto:
            nombre_adjunto = self.file_name
            IrAttachment = self.env['ir.attachment']
            data_attach = {
                'name': nombre_adjunto,
                'datas': self.adjunto,
                'type': 'binary',
                'description': nombre_adjunto,
                'res_model': "hr.expense",
                'res_id': expense_id.id,
            }
            new_attachment = IrAttachment.create(data_attach)

            data_attach2 = {
                'name': nombre_adjunto,
                'datas': self.adjunto,
                'type': 'binary',
                'description': nombre_adjunto,
                'res_model': "account.cashbox.session",
                'res_id': self.cashbox_session_id.id,
            }
            new_attachment2 = IrAttachment.create(data_attach2)

