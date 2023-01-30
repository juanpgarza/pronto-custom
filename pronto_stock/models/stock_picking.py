from odoo import models, api
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_cancel(self):        
        for rec in self.filtered(lambda x: x.state != 'cancel'):
            group = "pronto_stock.group_cancel_picking"
            if not rec.user_has_groups(group):
                group_id = self.env.ref(group)
                raise ValidationError("Opción habilitada solo para los miembros del grupo: \n\n'{} / {}'".format(group_id.sudo().category_id.name,group_id.name))
        return super(StockPicking, self).action_cancel()