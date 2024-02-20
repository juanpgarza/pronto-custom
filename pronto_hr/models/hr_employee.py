from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _anuncio_de_cumpleanios(self):

        empleados_activos = self.env['hr.employee'].search([])

        fecha_hoy = datetime.now().date()
        dia_hoy = fecha_hoy.day
        mes_hoy = fecha_hoy.month

        for rec in empleados_activos.filtered(lambda x: x.birthday):
            dia_cumple = rec.birthday.day
            mes_cumple = rec.birthday.month

            if dia_cumple == dia_hoy and mes_cumple == mes_hoy:
                values = {  'name': 'Hoy {} es el Cumple de {}!'.format(fecha_hoy.strftime('%d/%m/%Y'), rec.name),
                            'is_general_announcement': True,
                            'notification_date': datetime.now(),
                            'notification_expiry_date': datetime.now() + timedelta(days=1),
                            'active': True,
                }
                
                self.env['announcement'].create(values)
