# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import ValidationError,UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pricelist_item_ids = fields.Many2many(
        'product.pricelist.item', 'Item de Lista de Precios', compute='_get_pricelist_items')
    
    item_ids = fields.One2many('product.pricelist.item', 'product_tmpl_id', 'Pricelist Items')

    meses_de_stock = fields.Float("Meses de stock", compute="_compute_meses_de_stock", store=True)

    @api.depends('sales_count', 'virtual_available')
    def _compute_meses_de_stock(self):
        for rec in self:
            rec.meses_de_stock = rec.sales_count and rec.virtual_available / rec.sales_count * 12

    def _get_pricelist_items(self):
        for rec in self:
            item = rec.env['product.pricelist.item'].search([('product_tmpl_id', '=', rec.id)])

            if item:
                rec.pricelist_item_ids = item[0]
            else:
                rec.pricelist_item_ids = False

    @api.model
    def default_get(self, fields):
        rec = super(ProductTemplate, self).default_get(fields)

        rec['excluir_calculo_markup'] = False        
        rec['route_ids'] = False        
        rec['tracking'] = False
        rec['taxes_id'] = False
        rec['supplier_taxes_id'] = False

        return rec

    @api.model
    def create(self,values):

        if not values['tracking']:
            # este campo es obligatorio a nivel de base de datos
            # hay que informarlo aunque no se marque el producto como vendible
            if values['detailed_type'] == 'product':
                raise ValidationError("Debe informar el campo Seguimiento (Inventario/Trazabilidad)")
            else:
                values['tracking'] = 'none'

        if not self.user_has_groups('pronto.group_no_exigir_campos_producto_vendible'):
            mensaje_validacion = ""
            if values['sale_ok'] and values['type'] == 'product':

                if not values['excluir_calculo_markup']:
                    mensaje_validacion += "- Excluir del cálculo del markup \n"

                if not values['route_ids']:
                    mensaje_validacion += "- Rutas \n"

                if not self.taxes_id:
                    mensaje_validacion += "- Impuestos cliente \n"

                if not self.supplier_taxes_id:
                    mensaje_validacion += "- Impuestos de proveedor \n"

            if mensaje_validacion:
                raise ValidationError("Debe completar los siguientes campos para que el producto pueda ser vendido: \n\n" + mensaje_validacion)

        res = super(ProductTemplate,self).create(values)

        return res

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

                        if not self.taxes_id:
                            mensaje_validacion += "- Impuestos cliente \n"

                        if not self.supplier_taxes_id:
                            mensaje_validacion += "- Impuestos de proveedor \n"

                    if mensaje_validacion:
                        detalle_mensaje = mensaje_validacion
                        mensaje_validacion = ""
                        raise ValidationError("Ref. Interna: {} \n\n Debe completar los siguientes campos para que el producto pueda ser vendido: \n\n {}".format(
                                                    rec.default_code,
                                                    detalle_mensaje
                                            ))

    @api.depends('type')
    def _compute_tracking(self):
        super(ProductTemplate, self)._compute_tracking()
        self.tracking = False        