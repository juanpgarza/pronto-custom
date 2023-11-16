from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountPaymentCancelWizard(models.TransientModel):
    _name = 'account.payment.cancel.wizard'
    _description = 'Cancelar Pago'

    payment_group_id = fields.Many2one('account.payment.group',"Recibo")
    cancel_reason_note = fields.Char("Detalle el motivo de la cancelación")
    
    @api.model
    def default_get(self, field_names):
        defaults = super(AccountPaymentCancelWizard, self).default_get(field_names)
        defaults['payment_group_id'] = self.env.context['active_id']
        return defaults

    def do_cancel(self):
        if self.payment_group_id.state == 'cancel':
            raise UserError('El recibo ya fue cancelado')

        # AccountCashboxCancel = self.env['account.cashbox.cancel']

        self.env['account.cashbox.cancel'].create({
                                        'cancel_payment_group_id': self.payment_group_id.id,
                                        })

        self.payment_group_id.write({'cancel_reason_note': self.cancel_reason_note})
        # primero lo paso a borrador porque en el mod de adhoc
        # el botón de cancelar te lo muestra solo en el estado borrador
        self.payment_group_id.action_draft()
        self.payment_group_id.cancel()
