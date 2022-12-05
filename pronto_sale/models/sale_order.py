from odoo import models, fields
from odoo.exceptions import ValidationError,UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

