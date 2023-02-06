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

    @api.model
    def default_get(self, fields):
        rec = super(SaleOrder, self).default_get(fields)
        # Tarea #974
        # rec['user_id'] = False
        return rec

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        # Tarea #974
        # Se anula la funcion que hace que tome el comercial asignado al cliente
        # Lo informan a mano         
        user_id = self.user_id
        # import pdb; pdb.set_trace()
        res = super(SaleOrder, self).onchange_partner_id()
        # if user_id:
        #     import pdb; pdb.set_trace()
        self.update({'user_id': user_id.id})
        return res