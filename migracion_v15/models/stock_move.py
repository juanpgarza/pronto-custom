# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    # @api.model
    # def default_get(self, defaul_fields):
    #     res = super().default_get(defaul_fields)
    #     # import pdb; pdb.set_trace()
    #     if not res.get('product_uom'):
    #         res['product_uom'] = 1
    #     if not res.get('name'):
    #         res['name'] = "algo"
    #     # if not res.get('location_dest_id'):
    #     #     res['location_dest_id'] = 5            
    #     return res

    def write(self, vals):
        if 'product_uom' in vals:
            return True
        # import pdb; pdb.set_trace()
        return super().write(vals)