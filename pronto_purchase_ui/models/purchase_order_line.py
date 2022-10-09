# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import ValidationError

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_available = fields.Float("Cantidad a mano", related='product_id.qty_available')
    virtual_available = fields.Float("Cantidad prevista", related='product_id.virtual_available')

    vendor_invoice_price_unit = fields.Float("Precio Unitario Facturado", compute="_compute_invoice_price_unit")
    cost_price_unit = fields.Char("Precio de costo", compute="_compute_cost_price_unit")

    @api.one
    @api.depends('order_id.invoice_ids.invoice_line_ids.price_unit')
    def _compute_invoice_price_unit(self):
        self.vendor_invoice_price_unit = self.order_id.invoice_ids.invoice_line_ids.filtered(lambda x: x.purchase_line_id.id == self.id).price_unit 
        cost_pricelist_id = self.company_id.product_pricelist_cost_id
        self.cost_price_unit = cost_pricelist_id.item_ids.filtered(lambda x: x.product_tmpl_id.id == self.product_id.product_tmpl_id.id).price

