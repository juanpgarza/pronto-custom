from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line', 'base.exception.method']
    _name = 'sale.order.line'

    def detect_exceptions(self):
        for rec in self:            
            if rec.qty_invoiced == 0:
                res = super(SaleOrderLine, rec).detect_exceptions()
                # import pdb; pdb.set_trace()
            else:
                # import pdb; pdb.set_trace()
                res = []

            return res