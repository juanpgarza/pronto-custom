from odoo import models, api, fields
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    precio_unitario_con_descuento = fields.Float('Precio unitario con descuento', compute="_compute_precio_unitario_con_descuento")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.order_id.sale_order_template_id:
            raise ValidationError("Antes de informar los productos debe informar la plantilla")

    @api.depends('product_id', 'price_unit', 'discount')
    def _compute_precio_unitario_con_descuento(self):
        for line in self:
            if line.discount > 0:
                line.precio_unitario_con_descuento = line.price_unit * (1 - (1/line.discount))
            else:
                line.precio_unitario_con_descuento = line.price_unit