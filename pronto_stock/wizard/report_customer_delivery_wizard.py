from odoo import models, fields, api

class ReportCustomerDeliveryWizard(models.TransientModel):
    _name = 'report.customer.delivery.wizard'
    _description = 'Wizard para generar el reporte de entregas a clientes'

    def generate_report(self):
        # Llamamos a get_report_data para generar los datos del reporte
        self.env['report.customer.delivery'].get_report_data()

        # Retornamos la acción para abrir la vista del reporte
        return {
            'type': 'ir.actions.act_window',
            'name': 'Entregas a cliente por ubicación (meses de stock)',
            'res_model': 'report.customer.delivery',
            'view_mode': 'list,form',
            'target': 'current',
        }
