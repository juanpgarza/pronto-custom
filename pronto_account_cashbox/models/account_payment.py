from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    cashbox_id = fields.Many2one(
        related='cashbox_session_id.cashbox_id',
        store=True,
    )

    reason_id = fields.Many2one(comodel_name="account.cashbox.payment.reason", string= 'Motivo de movimiento')

    cashbox_transfer_id  = fields.Many2one(comodel_name="account.cashbox.transfer", string= 'Transf. entre cajas')

    def _default_session(self):
        # para que le seleccione automáticamente una sesión.
        # porque para la mayoría de los usuarios solo va a existir una sesión activa
        # y no tiene sentido que la tenga que seleccionar siempre.
        sesiones_caja_autorizadas = self.env['account.cashbox.session'].search([('state','=','opened')]).filtered(lambda x: self.env.user in x.cashbox_id.allowed_res_users_ids)
        
        if sesiones_caja_autorizadas:
            return sesiones_caja_autorizadas[0]
        else:
            return False

    cashbox_session_id = fields.Many2one(default=_default_session)

    def _create_paired_internal_transfer_payment(self):
        # en la transferencias entre caja, necesito que generar el paired payment a mano
        create_paired_payment = self.env.context.get('create_paired_payment', True)
        if create_paired_payment:
            super(AccountPayment, self)._create_paired_internal_transfer_payment()

    def action_post(self):
        res = super().action_post()

        for rec in self:
            if rec.cashbox_session_id:               
                self.env['account.cashbox.session.line.transaction']._create_from_payment(rec)
                
        return res

        