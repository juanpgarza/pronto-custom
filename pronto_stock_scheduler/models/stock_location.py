# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class StockLocation(models.Model):
    _inherit = "stock.location"

    usuario_responsable_reserva_stock_id = fields.Many2one('res.users',string="Resp. reservas de stock")
