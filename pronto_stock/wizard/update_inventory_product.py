from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import base64
from io import BytesIO
from xlrd import open_workbook

class UpdateInventoryProduct(models.TransientModel):
    _name = 'update.inventory.product'
    _description = 'Actualización de productos del inventario'

    inventory_id = fields.Many2one('stock.inventory',string='Inventario')
    excel_file_for_import = fields.Binary("Archivo")

    @api.model
    def default_get(self, field_names):
        defaults = super(
            UpdateInventoryProduct, self).default_get(field_names)
        defaults['inventory_id'] = self.env.context['active_id']
        return defaults
    
    def do_update(self):
        try:
            if self.inventory_id.state != 'draft':
                raise UserError('El inventario debe estar en el estado Borrador')
            if not self.inventory_id.location_ids:
                raise UserError('Debe informar una ubicación')
            inputx = BytesIO()
            inputx.write(base64.decodestring(self.excel_file_for_import))
            book = open_workbook(file_contents=inputx.getvalue())
        except TypeError as e:
            raise UserError(u'ERROR: {}'.format(e))

        sheet = book.sheets()[0]
        
        Quant =self.env['stock.quant']
        product_ids = []
        for i in list(range(sheet.nrows)):
            default_code = sheet.cell(i, 0).value
            if not default_code:
                raise UserError('ERROR: {}'.format("No se informó el código para la linea", i))
            # import pdb; pdb.set_trace()
            product = self.env['product.product'].search([('default_code','=',int(default_code))])
            if not product:
                raise UserError("El producto con código %s no existe. No se realizará ninguna actualización." % default_code)

            cantidad_contada = sheet.cell(i, 1).value

            # import pdb; pdb.set_trace()
            product_ids.append(product.id)
            # product_ids = product_ids + product.id
            for rec in self.inventory_id.location_ids:
                quant = Quant.search(['&',('product_id','=',product.id),('location_id','=',rec.id)])
                if not quant:
                    # crear el quant
                    new_quant = Quant.create({'product_id': product.id,
                                            'location_id': rec.id,
                                            'inventory_quantity': cantidad_contada,
                                            'user_id': self.env.user.id,
                                            'inventory_quantity_set': True})

                    # import pdb; pdb.set_trace()
                else:
                    # el quant ya existe. Lo tengo que actualizar con la cantidad contada
                    quant.write({'inventory_quantity': cantidad_contada,
                                 'inventory_quantity_set': True})

        self.inventory_id.product_selection = 'manual'

        self.inventory_id["product_ids"] = [(6, 0, product_ids)]
        
        return

    