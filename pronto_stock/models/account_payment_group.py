from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime

class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    def post(self):
        res = super().post()
        # tengo que controlar que sea [('partner_type', '=', 'customer')] el AccountPaymentGroup
        for rec in self.matched_move_line_ids:
            # filtrar para que sea una factura (no una NC)
            if rec.move_id.payment_state in ('in_payment','paid'):
                # puedo buscar los pickings que tiene asociada esta factura (ver sale_invoice_ids en ESTE modulo)
                # y si todas las facturas estan como pagadas, le cargo la actividad
                # tambien tengo que mirar la fecha de la factura. si es la misma que el recibo, NO se carga actividad.
                # eso se pago enseguida, no hace falta avisar 
                import pdb; pdb.set_trace()
        return res
    