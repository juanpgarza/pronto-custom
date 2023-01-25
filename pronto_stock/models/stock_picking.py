from odoo import models, api
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_cancel(self):        
        for rec in self:
            if not rec.user_has_groups('pronto_stock.group_cancel_picking'):
                raise ValidationError("No posee permisos suficientes para cancelar el movimiento \n\n")
        return super(StockPicking, self).action_cancel()