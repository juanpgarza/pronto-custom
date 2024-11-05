from odoo import models, api, fields
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    precio_unitario_con_descuento = fields.Float('Precio unitario con descuento', compute="_compute_precio_unitario_con_descuento")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.order_id.sale_order_template_id:
            raise ValidationError("Antes de informar los productos debe informar la plantilla")

    @api.depends('product_id', 'price_unit', 'discount')
    def _compute_precio_unitario_con_descuento(self):
        for line in self:
            line.precio_unitario_con_descuento = line.price_unit * (1 - (line.discount/100))

    # @api.onchange('product_id')
    # def _onchange_product_id_add_accessories(self):
        
    #     # import pdb; pdb.set_trace()
    #     """Agregar productos accesorios cuando se selecciona o modifica el producto de la línea."""
    #     if not self.order_id or not self.product_id:
    #         return
        
    #     # Eliminar opciones actuales para esta línea
    #     existing_options = self.env['sale.order.option'].search([
    #         ('order_id', '=', self.order_id.id),
    #         ('line_id', '=', self.id)
    #     ])
    #     existing_options.unlink()
    #     import pdb; pdb.set_trace()
    #     # Obtener productos accesorios que estén disponibles para la venta
    #     accessory_products = self.product_id.accessory_product_ids.filtered(lambda p: p.sale_ok)

    #     # Crear opciones de productos accesorios
    #     for accessory in accessory_products:
    #         import pdb; pdb.set_trace()
    #         self.env['sale.order.option'].create({
    #             'order_id': self.order_id.id,                # ID de la orden de venta
    #             'line_id': self.id,                          # ID de la línea de pedido
    #             'product_id': accessory.id,                  # Producto accesorio
    #             'name': accessory.display_name,              # Nombre del accesorio
    #             'uom_id': accessory.uom_id.id,               # Unidad de medida del accesorio
    #             'price_unit': accessory.lst_price,           # Precio del accesorio
    #             'quantity': 1.0                              # Cantidad predeterminada
    #         })

    @api.model
    def create(self, vals):
        # Crear la línea de pedido
        line = super(SaleOrderLine, self).create(vals)
        
        # Agregar productos accesorios después de crear la línea
        line._add_accessory_products()
        
        return line

    def write(self, vals):
        # Actualizar la línea de pedido
        res = super(SaleOrderLine, self).write(vals)
        for line in self:
            # existing_options = self.env['sale.order.option'].search([('order_id', '=', line.order_id.id), ('line_id', '=', line.id)])
            # existing_options.unlink()

            # Agregar o actualizar productos accesorios después de modificar la línea
            self._add_accessory_products()
        
        return res

    def unlink(self):
        # Lógica adicional antes de eliminar la línea de pedido
        for line in self:
            # Eliminar los productos accesorios asociados a esta línea de pedido
            accessory_options = self.env['sale.order.option'].search([
                ('order_id', '=', line.order_id.id),
                ('line_id', '=', line.id)
            ])
            accessory_options.unlink()  # Elimina las opciones de accesorios asociadas
        
        # Llamar al método unlink original para eliminar la línea de pedido
        return super(SaleOrderLine, self).unlink()
    
    def _add_accessory_products(self):
        
        """Agregar productos accesorios cuando se crea o modifica una línea de pedido."""
        for line in self:
            # Verificar que la línea tenga un pedido y un producto
            if not line.order_id or not line.product_id:
                continue
            
            # Eliminar opciones actuales para esta línea
            # existing_options = self.env['sale.order.option'].search([
            #     ('order_id', '=', line.order_id.id),
            #     ('line_id', '=', line.id)
            # ])
            # existing_options.unlink()

            # Obtener productos accesorios que estén disponibles para la venta
            accessory_products = line.product_id.accessory_product_ids.filtered(lambda p: p.sale_ok)

            # Crear opciones de productos accesorios
            for accessory in accessory_products:
                self.env['sale.order.option'].create({
                    'order_id': line.order_id.id,                # ID de la orden de venta
                    'line_id': line.id,                          # ID de la línea de pedido
                    'product_id': accessory.id,                  # Producto accesorio
                    'name': accessory.display_name,              # Nombre del accesorio
                    'uom_id': accessory.uom_id.id,               # Unidad de medida del accesorio
                    'price_unit': accessory.lst_price,           # Precio del accesorio
                    'quantity': 1.0                              # Cantidad predeterminada
                })
