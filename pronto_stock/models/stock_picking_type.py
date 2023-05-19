from odoo import models, api
from odoo.exceptions import ValidationError

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    # con esto evito que al navegar desde una tarjeta del kanban de tipos de operación
    # me oculte el campo tipo de operación en el form de transferencias de stock
    # src/addons/stock/models/stock_picking.py    
    def _get_action(self, action_xmlid):
        res = super(StockPickingType,self)._get_action(action_xmlid)
        res['context'].pop('default_picking_type_id')
        return res