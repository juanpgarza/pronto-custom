from odoo import models, fields
from odoo.exceptions import ValidationError

class AccountCashboxSession(models.Model):
    _inherit = 'account.cashbox.session'

    arqueo_inicial_realizado = fields.Boolean('Arqueo realizado',default=False)

    def action_account_cashbox_session_open(self):
        super(AccountCashboxSession,self).action_account_cashbox_session_open()
        for session in self:
            if not session.arqueo_inicial_realizado:
                raise ValidationError("El arqueo inicial está pendiente.")
