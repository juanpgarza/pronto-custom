from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_cancel(self):        
        for rec in self:
            if not rec.user_has_groups('pronto_sale.group_cancel_sale_order'):
                raise ValidationError("No posee permisos suficientes para cancelar el pedido \n\n")
        return super(SaleOrder, self).action_cancel()