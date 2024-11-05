from odoo import models, api

class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    # sobre-escribo el metodo. pongo todos en True para que no los muestre en el presu web
    @api.depends('line_id', 'order_id.order_line', 'product_id')
    def _compute_is_present(self):        
        for option in self:            
            option.is_present = True