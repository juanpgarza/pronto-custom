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

    def _multi_line_quantity_done_set(self, quantity_done):
        move_lines = self._get_move_lines()
        # Bypass the error if we're trying to write the same value.
        ml_quantity_done = 0
        for move_line in move_lines:
            ml_quantity_done += move_line.product_uom_id._compute_quantity(move_line.qty_done, self.product_uom, round=False)
        # if float_compare(quantity_done, ml_quantity_done, precision_rounding=self.product_uom.rounding) != 0:
        #     raise UserError(_("Cannot set the done quantity from this stock move, work directly with the move lines."))

    # def write(self, vals):
    #     if 'product_uom' in vals:
    #         return True
    #     # import pdb; pdb.set_trace()
    #     return super().write(vals)

    # def _action_assign(self):
    #     import wdb; wdb.set_trace()
    #     # para que no genere el stock.move.line
    #     return True
