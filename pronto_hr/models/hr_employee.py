from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    fecha_ingreso = fields.Date("Fecha de Ingreso", groups="hr.group_hr_user")

    def _anuncio_de_cumpleanios_aniversario(self):

        empleados_activos = self.env['hr.employee'].search([])

        fecha_hoy = datetime.now().date()
        dia_hoy = fecha_hoy.day
        mes_hoy = fecha_hoy.month

        # TODO: que tome la configuración del anuncio archivado
        anuncio_cumpleanio = self.env.ref('pronto_hr.announcement_cumpleanio')
        for rec in empleados_activos.filtered(lambda x: x.birthday):
            dia_cumple = rec.birthday.day
            mes_cumple = rec.birthday.month

            if dia_cumple == dia_hoy and mes_cumple == mes_hoy:
                values = {  'name': anuncio_cumpleanio.name,
                            'content': anuncio_cumpleanio.content.format(fecha_hoy.strftime('%d/%m/%Y'), rec.name),
                            'is_general_announcement': True,
                            'notification_date': datetime.now(),
                            'notification_expiry_date': datetime.now() + timedelta(days=1),
                            'active': True,
                }
                
                self.env['announcement'].create(values)

        # TODO: que tome la configuración del anuncio archivado
        anuncio_aniversario = self.env.ref('pronto_hr.announcement_aniversario')
        for rec in empleados_activos.filtered(lambda x: x.fecha_ingreso):
            dia_aniversario = rec.fecha_ingreso.day
            mes_aniversario = rec.fecha_ingreso.month

            if dia_aniversario == dia_hoy and mes_aniversario == mes_hoy:
                values = {  'name': anuncio_aniversario.name,
                            'content': anuncio_aniversario.content.format(fecha_hoy.strftime('%d/%m/%Y'), rec.name),
                            'is_general_announcement': True,
                            'notification_date': datetime.now(),
                            'notification_expiry_date': datetime.now() + timedelta(days=1),
                            'active': True,
                }
                
                self.env['announcement'].create(values)
