from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountCashboxTransferReceiveWizard(models.TransientModel):
    _name = 'account.cashbox.transfer.receive.wizard'
    _description = 'Transferencia'

    cashbox_session_id = fields.Many2one('account.cashbox.session', string='Sesión')
    session_cash_control_journal_ids = fields.Many2many('account.journal', related='cashbox_session_id.session_cash_control_journal_ids')
    cashbox_id = fields.Many2one('account.cashbox', related='cashbox_session_id.cashbox_id')

    cashbox_transfer_id  = fields.Many2one(
                    comodel_name="account.cashbox.transfer", 
                    string= 'Transf. entre cajas', 
                    domain="[('destination_cashbox_id', '=', cashbox_id),('state','=','sent')]")

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


    @api.model
    def default_get(self, field_names):
        defaults = super(AccountCashboxTransferReceiveWizard, self).default_get(field_names)
        defaults['cashbox_session_id'] = self.env.context['active_id']
        return defaults

    def do_transfer_receive(self):
        
        if self.cashbox_session_id.state != 'opened':
            raise ValidationError("La sesión de estar Abierta para poder recibir una transferencia")
        
        origin_payment_id = self.cashbox_transfer_id.origin_payment_id

        origin_payment_id.with_context(recibiendo_transferencia=True)._create_paired_internal_transfer_payment()

        paired_payment_id = origin_payment_id.paired_internal_transfer_payment_id

        paired_payment_id.cashbox_session_id = self.cashbox_session_id
        
        self.cashbox_transfer_id.destination_payment_id = paired_payment_id

        self.cashbox_transfer_id.write({
            'destination_payment_id': paired_payment_id.id,
            'state': 'received',
        })
        return