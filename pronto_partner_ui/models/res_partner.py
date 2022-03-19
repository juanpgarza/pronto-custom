# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_product_pricelist = fields.Many2one(store=True)

    def write(self, values):
        super(ResPartner,self).write(values)
        if 'sale_type' in values:
            if not self.user_has_groups('pronto_partner_ui.group_ventas_cambiar_tipo_venta_contacto'):
                create_from_website = self._context.get('create_from_website', False)
                if not create_from_website:
                    raise ValidationError("Su usuario no posee permisos para modificar el tipo de venta")
