# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _name = "purchase.order"    
    _inherit = ['purchase.order', 'tier.validation']

    date_planned_reconfirmed = fields.Boolean('Fecha prevista re-confirmada')

    @api.multi
    def button_confirm(self):
        for order in self:
            if not order.date_planned_reconfirmed:
                raise ValidationError("Debe re-confirmar la fecha prevista para poder confirmar el pedido de compra")

        return super(PurchaseOrder, self).button_confirm()

    @api.model
    def _get_under_validation_exceptions(self):
        res = super(PurchaseOrder,self)._get_under_validation_exceptions()
        # estos campos no los va a tener en cuenta para la validación
        res.append('date_planned_reconfirmed')
        return res