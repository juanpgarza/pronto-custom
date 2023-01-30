from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_cancel(self):        
        # solo para pedidos de venta. NO incluye presupuestos
        for rec in self.filtered(lambda x:x.state in ('done','sale') and x.state != 'cancel'):
            group = "pronto_sale.group_cancel_sale_order"
            if not rec.user_has_groups(group):
                group_id = self.env.ref(group)
                raise ValidationError("Opción habilitada solo para los miembros del grupo: \n\n'{} / {}'".format(group_id.sudo().category_id.name,group_id.name))
        return super(SaleOrder, self).action_cancel()