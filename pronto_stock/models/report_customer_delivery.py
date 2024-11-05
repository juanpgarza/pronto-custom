from odoo import models, fields, api
from datetime import datetime, timedelta

class ReportCustomerDelivery(models.TransientModel):
    _name = 'report.customer.delivery'
    _description = 'Entregas a cliente por ubicación (meses de stock)'
    _rec_name = 'product_id'

    # Campos para la vista del reporte
    product_id = fields.Many2one('product.product', string='Producto')
    location_id = fields.Many2one('stock.location', string='Ubicación de Origen')
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacén')  # Nuevo campo de almacén
    quantity = fields.Float(string='Cantidad Entregada ultimos 365 días')
    forecasted_quantity = fields.Float(string='Cantidad Pronosticada')
    meses_stock = fields.Float(string='Meses de Stock')

    @api.model
    def get_report_data(self):
        
        # Fecha de inicio (hace 365 días desde hoy)
        date_from = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        # Consulta para obtener movimientos de entrega a clientes, agrupados por producto y ubicación de origen
        self.env.cr.execute("""
            SELECT
                product_id,
                location_id,
                SUM(product_qty) AS quantity
            FROM
                stock_move
            WHERE
                state = 'done'
                AND location_dest_id IN (SELECT id FROM stock_location WHERE usage = 'customer')
                            AND date >= %s
            GROUP BY
                product_id, location_id
        """, (date_from,))
        stock_data = self.env.cr.fetchall()

        # Crear una lista para almacenar los registros que se van a crear
        report_data = []

        # Procesar cada grupo de producto y ubicación
        for product_id, location_id, quantity in stock_data:
            # Obtener la cantidad pronosticada (virtual_available) del producto en la ubicación
            product = self.env['product.product'].browse(product_id)
            forecasted_qty = product.with_context(location=location_id).virtual_available

            # Calcular meses_stock: (forecasted_quantity / quantity) * 12
            # Asegurarse de que quantity no sea cero para evitar división por cero
            meses_stock = (forecasted_qty / quantity * 12) if quantity else 0

            # Obtener el almacén relacionado con la ubicación
            location = self.env['stock.location'].browse(location_id)
            warehouse = self.env['stock.warehouse'].search([('view_location_id', 'parent_of', location_id)], limit=1)

            # Agregar los datos a la lista
            report_data.append({
                'product_id': product_id,
                'location_id': location_id,
                'warehouse_id': warehouse.id if warehouse else False,  # Si no hay almacén, lo dejamos vacío
                'quantity': quantity,
                'forecasted_quantity': forecasted_qty,
                'meses_stock': meses_stock,
            })

        # Limpiar datos previos y crear los nuevos registros
        self.env['report.customer.delivery'].search([]).unlink()  # Limpiar registros previos
        for data in report_data:
            self.create(data)

        # Retorna los registros para mostrarlos en una vista (puedes usar un wizard o simplemente una vista tree)
        return self.search([])
