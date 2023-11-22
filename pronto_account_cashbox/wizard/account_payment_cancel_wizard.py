from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountPaymentCancelWizard(models.TransientModel):
    _name = 'account.payment.cancel.wizard'
    _description = 'Cancelar Pago'

    payment_group_id = fields.Many2one('account.payment.group',"Recibo")
    cancel_reason_note = fields.Char("Detalle el motivo de la cancelación")
    
    # vienen de la caja de v12
    pago_con_sesion_informada = fields.Boolean("Con sesión informada", compute="_compute_sesion_informada", store=True)

    @api.depends('payment_group_id')
    def _compute_sesion_informada(self):
        if self.payment_group_id.cashbox_session_id:
            self.pago_con_sesion_informada = True
            # import pdb; pdb.set_trace()
        else:
            self.pago_con_sesion_informada = False
            # import pdb; pdb.set_trace()

    cashbox_id = fields.Many2one(
        'account.cashbox', 
        string='Caja objetivo cancelación',
        )
    
    @api.model
    def default_get(self, field_names):
        defaults = super(AccountPaymentCancelWizard, self).default_get(field_names)
        defaults['payment_group_id'] = self.env.context['active_id']
        return defaults

    def do_cancel(self):
        if self.payment_group_id.state == 'cancel':
            raise UserError('El recibo ya fue cancelado')



        # AccountCashboxCancel = self.env['account.cashbox.cancel']

        new_acc = self.env['account.cashbox.cancel'].create({
                                        'cancel_payment_group_id': self.payment_group_id.id,
                                        })

        new_acc.matched_move_line_ids = self.payment_group_id.matched_move_line_ids
        
        self.payment_group_id.write({'cancel_reason_note': self.cancel_reason_note})

        if not self.pago_con_sesion_informada:
            # import pdb; pdb.set_trace()
            # son los recibos/OP que se cargaron en v12 (y las cajas y sus sesiones no se migraron)
            # se deja el registro de la cancelación en la caja FSM
            self.cashbox_id = self.env.ref('pronto_account_cashbox.account_cashbox_caja_fsm')
            if not self.cashbox_id.current_session_id:
                raise UserError('Debe iniciar una sesión de la caja: "{}"'.format(self.cashbox_id.name))
            
            self.payment_group_id.payment_ids.write({'cashbox_session_id': self.cashbox_id.current_session_id.id})
            for rec in self.payment_group_id.payment_ids:
                self.env['account.cashbox.session.line.transaction']._create_from_payment(rec)

        # primero lo paso a borrador porque en el mod de adhoc
        # el botón de cancelar te lo muestra solo en el estado borrador
        self.payment_group_id.action_draft()
        self.payment_group_id.cancel()
