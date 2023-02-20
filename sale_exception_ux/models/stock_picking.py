# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def write(self, values):
        if 'state' in values and values['state'] == 'done':
            if self.picking_type_id.code == 'outgoing' and self.sale_id.main_exception_id:
                raise ValidationError('Se debe resolver la excepción en el pedido')
        super(StockPicking,self).write(values)