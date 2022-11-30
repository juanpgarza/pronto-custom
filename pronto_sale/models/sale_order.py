from odoo import models, fields
from odoo.exceptions import ValidationError,UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # lo uso en una validación de nivel de tipo Fórmula.
    # el código para controlar la fecha de vencimiento es: not rec.valid_quotation()
    def valid_quotation(self):
        for rec in self:
            delta = rec.validity_date - fields.Date.context_today(self)

            if delta.days >= 0:
                return True
            else:
                return False
