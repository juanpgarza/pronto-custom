# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.exceptions import ValidationError,UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def default_get(self, fields):
        rec = super(ProductTemplate, self).default_get(fields)

        # rec['excluir_calculo_markup'] = False
        rec['route_ids'] = False
        rec['tracking'] = False

        return rec

    @api.onchange('detailed_type')
    def onchange_detailed_type(self):
        if self.detailed_type == 'product':
            self.tracking = False

    @api.model
    def create(self,values):

        if not values['tracking']:
            # este campo es obligatorio a nivel de base de datos
            # hay que informarlo aunque no se marque el producto como vendible
            raise ValidationError("Debe informar el campo Seguimiento (Inventario/Trazabilidad)")

        if not self.user_has_groups('pronto_product_ui.group_no_exigir_campos_producto_vendible'):
            mensaje_validacion = ""
            if values['sale_ok'] and values['type'] == 'product':
                # import wdb; wdb.set_trace()
                if 'weight' in values and values['weight'] == 0:
                    mensaje_validacion += "- peso \n"
                if 'weight' in values and values['volume'] == 0:
                    mensaje_validacion += "- volumen \n"
                if not values['image_1920']:
                    mensaje_validacion += "- imagen del producto \n"
                if not values['barcode']:
                    mensaje_validacion += "- codigo de barras \n"

                # item_lista_precio = self.item_ids.filtered(lambda x: x.pricelist_id.id == 2)
                # if not item_lista_precio:
                #     mensaje_validacion += "- precio en la tarifa Costo \n"

                proveedores = self.seller_ids
                if not proveedores:
                    mensaje_validacion += "- Proveedor \n"

                # if not values['excluir_calculo_markup']:
                #     mensaje_validacion += "- Excluir del cálculo del markup \n"

                if not self.route_ids:
                    mensaje_validacion += "- Rutas \n"

            if mensaje_validacion:
                raise ValidationError("Debe completar los siguientes campos para que el producto pueda ser vendido: \n\n" + mensaje_validacion)

        res = super(ProductTemplate,self).create(values)

        return res

    def write(self, values):
        super(ProductTemplate,self).write(values)

        controlar_requeridos = self.env.context.get('controlar_requeridos', True)

        if controlar_requeridos:
            # import wdb; wdb.set_trace()
            if not self.user_has_groups('pronto_product_ui.group_no_exigir_campos_producto_vendible'):
                for rec in self:
                    mensaje_validacion = ""

                    if rec.type == 'product' and rec.sale_ok:

                        # if not rec.excluir_calculo_markup:
                        #     mensaje_validacion += "- Excluir del cálculo del markup \n"

                        if not rec.route_ids:
                            mensaje_validacion += "- Rutas \n"

                    if mensaje_validacion:
                        detalle_mensaje = mensaje_validacion
                        mensaje_validacion = ""
                        raise ValidationError("Ref. Interna: {} \n\n Debe completar los siguientes campos para que el producto pueda ser vendido: \n\n {}".format(
                                                    rec.default_code,
                                                    detalle_mensaje
                                            ))
