from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date

class AccountMove(models.Model):
    _inherit = 'account.move'

    vencida = fields.Boolean(string = 'Is Expired', compute = '_compute_vencida', search = '_search_vencida')

    def _compute_vencida(self):
        now = fields.Datetime.now()
        for rec in self:
            if rec.move_type == 'out_invoice' and rec.state == 'posted' and rec.payment_state in ('not_paid','partial'):
                rec.vencida = now.date() > rec.invoice_date_due
            else:
                rec.vencida = False
            
    def _search_vencida(self, operator, value):
        now = fields.Datetime.now()
        facturas = self.env['account.move'].search([])        
        ids = facturas.filtered(lambda x: x.move_type == 'out_invoice' and x.state == 'posted' and x.payment_state in ('not_paid','partial')).mapped('id')
        return [('id', 'in', ids)]

    def _dias_atraso(self):
        fecha_vencimiento = self.invoice_date_due            
        delta = datetime.now().date() - fecha_vencimiento
        return delta.days

    @api.model
    def facturas_atrasadas(self, dias_atraso):
        res = self.search([('vencida','=',True)])
        # import pdb; pdb.set_trace()
        # len(self.env['account.move'].facturas_atrasadas(90))
        return res.filtered(lambda x: x._dias_atraso() > dias_atraso)