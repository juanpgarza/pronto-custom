# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPickingVoucher(models.Model):
    _inherit = 'stock.picking.voucher'

    picking_id = fields.Many2one(
        required=False,
    )
