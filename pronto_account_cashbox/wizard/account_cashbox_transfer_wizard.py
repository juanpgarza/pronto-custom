from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountCashboxTransferWizard(models.TransientModel):
    _name = 'account.cashbox.transfer.wizard'
    _description = 'Transferencia'

    # tipo_de_movimiento = fields.Selection([('recibo', 'Recibo'),
    #      ('pago', 'Pago'),
    #      ('gasto', 'Gasto')],
    #     string="Tipo de Movimiento",)

    cashbox_session_id = fields.Many2one('account.cashbox.session', string='Sesión')
    session_cash_control_journal_ids = fields.Many2many('account.journal', related='cashbox_session_id.session_cash_control_journal_ids')
    cashbox_id = fields.Many2one('account.cashbox', related='cashbox_session_id.cashbox_id')

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

    # destination_cashbox_id = fields.Many2one('account.cashbox', string='Caja destino', required=True, domain="[('id','!=',cashbox_id)]")

    ref = fields.Char(string='Referencia')

    cashbox_search = fields.Char("Buscar caja destino")
    cashbox_found = fields.Char("Caja destino")

    def _get_destination_cashbox_id(self):
        # self.destination_cashbox = 0
        if self.cashbox_search and len(self.cashbox_search) >= 3:
            # import pdb; pdb.set_trace()
            Account_cashbox = self.env["account.cashbox"].sudo().search([('name','ilike',self.cashbox_search)])
            if len(Account_cashbox) == 1:
                self.cashbox_found = Account_cashbox.name
                # self.destination_cashbox = Account_cashbox.id
                # import pdb; pdb.set_trace()
                return Account_cashbox
            else:
                self.cashbox_found = Account_cashbox.mapped("name")
                return False
        else:
            return False

    @api.onchange("cashbox_search")
    def onchange_cashbox_search(self):
        self._get_destination_cashbox_id()

    @api.model
    def default_get(self, field_names):
        defaults = super(AccountCashboxTransferWizard, self).default_get(field_names)
        defaults['cashbox_session_id'] = self.env.context['active_id']
        return defaults

    def do_transfer(self):

        if self.cashbox_session_id.state in ('draft','closed'):
            raise UserError('Debe iniciar sesión de caja para realizar este movimiento.')

        if self.unit_amount == 0:
            raise UserError('El importe no puede ser cero.')

        if not self._get_destination_cashbox_id():
            self.cashbox_search = ""
            raise UserError('Debe informar la caja destino.')
        
        # if self.tipo_de_movimiento in ('pago','gasto'):
        #     partner_id = self.env.ref('pronto_account_cashbox.proveedor_no_habitual')
        #     payment_type = 'outbound'
        #     partner_type = 'supplier'
            
        # else:
        #     partner_id = self.env.ref('pronto_account_cashbox.cliente_generico')
        #     payment_type = 'inbound'
        #     partner_type = 'customer'

        payment_vals = {
            'amount': self.unit_amount,
            'payment_type': 'outbound',
            # 'partner_type': partner_type,
            'journal_id': self.journal_id.id,
            'partner_id': self.journal_id.company_id.partner_id.id,
            'payment_method_line_id': self.journal_id._get_available_payment_method_lines('outbound').filtered(lambda x: x.code == 'manual').id,
            'cashbox_session_id': self.cashbox_session_id.id,
            'ref': self.ref,
            'destination_journal_id': self._get_destination_cashbox_id().cash_control_journal_ids.filtered(lambda x: x.currency_id == self.journal_id.currency_id)[0].id,
        }
        payment = self.env['account.payment'].with_context(create_paired_payment=False).create(payment_vals)

        transfer_vals = {
            'state': 'sent',
            'origin_payment_id': payment.id,
            'destination_cashbox_id': self._get_destination_cashbox_id().id,
        }

        transfer = self.env['account.cashbox.transfer'].sudo().create(transfer_vals)

        payment.write({'cashbox_transfer_id': transfer.id })
        payment.action_post()