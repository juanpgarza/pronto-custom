from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.order_id.sale_order_template_id:
            raise ValidationError("Antes de informar los productos debe informar la plantilla")
