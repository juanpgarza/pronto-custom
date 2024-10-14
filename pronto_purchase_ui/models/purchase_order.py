# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _name = "purchase.order"    
    _inherit = ['purchase.order', 'tier.validation']

    date_planned_reconfirmed = fields.Boolean('Fecha prevista re-confirmada')

    proveedor_entrega_a = fields.Many2one("res.partner",string="Proveedor entrega a",domain=lambda self: self._get_dynamic_domain())

    def _get_dynamic_domain(self):
        # import pdb; pdb.set_trace()
        # self.env.user.company_id.partner_id.child_ids.mapped("id")
        return [('id', 'in', self.env.user.company_id.partner_id.child_ids.mapped("id"))]
    
    def button_confirm(self):
        for order in self:
            if not order.date_planned_reconfirmed:
                raise ValidationError("Debe re-confirmar la fecha prevista para poder confirmar el pedido de compra")
            for line in order.order_line:
                line.qty_available_static = line.product_id.qty_available
                line.virtual_available_static = line.product_id.virtual_available

        return super(PurchaseOrder, self).button_confirm()

    @api.model
    def _get_under_validation_exceptions(self):
        res = super(PurchaseOrder,self)._get_under_validation_exceptions()
        # estos campos no los va a tener en cuenta para la validación
        res.append('date_planned_reconfirmed')
        res.append('notes')
        res.append('internal_notes')
        return res