# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # src/addons/sale_stock/models/sale_order.py:
    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        # import pdb; pdb.set_trace()
        return True

    def _get_protected_fields(self):
        return []
