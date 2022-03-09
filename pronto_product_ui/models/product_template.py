# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.exceptions import ValidationError,UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def default_get(self, fields):
        rec = super(ProductTemplate, self).default_get(fields)

        rec['excluir_calculo_markup'] = False        
        rec['route_ids'] = False        
        rec['tracking'] = False

        return rec

    @api.model
    def create(self,values):

        if not values['tracking']:
            # este campo es obligatorio a nivel de base de datos
            # hay que informarlo aunque no se marque el producto como vendible
            raise ValidationError("Debe informar el campo Seguimiento (Inventario/Trazabilidad)")

        if not self.user_has_groups('pronto.group_no_exigir_campos_producto_vendible'):
            mensaje_validacion = ""
            if values['sale_ok'] and values['type'] == 'product':

                if not values['excluir_calculo_markup']:
                    mensaje_validacion += "- Excluir del cálculo del markup \n"

                if not self.route_ids:
                    mensaje_validacion += "- Rutas \n"

            if mensaje_validacion:
                raise ValidationError("Debe completar los siguientes campos para que el producto pueda ser vendido: \n\n" + mensaje_validacion)

        res = super(ProductTemplate,self).create(values)

        return res

    @api.multi
    def write(self, values):
        super(ProductTemplate,self).write(values)        
        
        controlar_requeridos = self.env.context.get('controlar_requeridos', True)

        if controlar_requeridos:
            if not self.user_has_groups('pronto.group_no_exigir_campos_producto_vendible'):
                for rec in self:
                    mensaje_validacion = ""

                    if rec.type == 'product' and rec.sale_ok:

                        if not rec.excluir_calculo_markup:
                            mensaje_validacion += "- Excluir del cálculo del markup \n"

                        if not rec.route_ids:
                            mensaje_validacion += "- Rutas \n"

                    if mensaje_validacion:
                        detalle_mensaje = mensaje_validacion
                        mensaje_validacion = ""
                        raise ValidationError("Ref. Interna: {} \n\n Debe completar los siguientes campos para que el producto pueda ser vendido: \n\n {}".format(
                                                    rec.default_code,
                                                    detalle_mensaje
                                            ))
