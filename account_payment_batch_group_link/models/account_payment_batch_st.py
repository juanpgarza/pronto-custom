from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date

class AccountPaymentBatchSt(models.Model):
    _inherit = 'account.payment.batch.st'

    payment_group_id = fields.Integer("Grupo de pago")

    payment_group_url = fields.Char("url grupo de pago", compute='_compute_payment_group_url')


    def _compute_payment_group_url(self):
        #  https://prontodistribuidora.ar/web#id=42762&menu_id=243&cids=1&action=450&model=account.payment.group&view_type=form
        url_v15 = self.env['ir.config_parameter'].get_param('account_payment_batch_group_link.url_v15')

        for rec in self:
            if rec.payment_group_id and url_v15:
                rec.payment_group_url = "%s/web#id=%d&menu_id=243&cids=1&action=450&model=account.payment.group&view_type=form" % (url_v15,rec.payment_group_id)
            else:
                rec.payment_group_url = ""
