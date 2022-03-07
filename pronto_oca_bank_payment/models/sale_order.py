# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.multi
    # def _action_confirm(self):
    #     super(SaleOrder, self)._action_confirm()
    #     for rec in self:
    #         if not rec.payment_mode_id:
    #             raise ValidationError("Debe informar el modo de pago ")

    @api.multi
    def write(self, values):
        # if self.user_has_groups('pronto.group_commitment_date_required'):
        if ('state' in values and self.state != 'done' and values['state'] == 'sale') or 'user_requesting_review' in values:
                if not self.payment_mode_id:
                    raise ValidationError(
                            'Debe informar el modo de pago'
                            )
        return super(SaleOrder, self).write(values)