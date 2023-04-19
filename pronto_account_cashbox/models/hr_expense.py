##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    cashbox_session_id = fields.Many2one('account.cashbox.session', related="payment_id.cashbox_session_id", string="Sesión de caja")

    payment_id = fields.Many2one(
        comodel_name='account.payment',
        string="Pago", copy=False)

    def unlink(self):
        for expense in self:
            if expense.payment_id:
                raise UserError(_('No se puede suprimir un gasto que ingreso desde una caja.'))
        super(HrExpense, self).unlink()