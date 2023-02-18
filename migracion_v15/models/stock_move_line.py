# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # este campo no existe en v12 y es obligatorio en v15
    # company_id = fields.Many2one(default=1)

    @api.model
    def default_get(self, defaul_fields):
        res = super().default_get(defaul_fields)
        # import pdb; pdb.set_trace()
        if not res.get('company_id'):
            res['company_id'] = 1
        # if not res.get('product_uom_id'):
        #     res['product_uom_id'] = 1
        # if not res.get('location_id'):
        #     res['location_id'] = 8
        # if not res.get('location_dest_id'):
        #     res['location_dest_id'] = 5
        return res
