# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    date_planned = fields.Datetime(compute=False)

    @api.multi
    def button_confirm(self):
        for order in self:
            if not order.date_planned:
                raise ValidationError("Debe informar la fecha prevista para poder confirmar el pedido de compra")

        return super(PurchaseOrder, self).button_confirm()