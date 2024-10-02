from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'


    def write(self, vals):
        # import pdb; pdb.set_trace()
        res = super().write(vals)
        if 'payment_state' in vals:
            raise ValidationError("Aca")

    @api.onchange('payment_state')
    def _onchange_payment_state(self):
        for rec in self:
            import pdb; pdb.set_trace()
            if rec.payment_state in ('in_payment','paid'):
                raise ValidationError("Aca")
