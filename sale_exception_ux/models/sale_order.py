# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # 1 - Descuentos - Productos simple
    def check_discount_simple_product(self):
        self.ensure_one()
        for line in self.order_line:
            if line.discount > 4 and line.qty_invoiced == 0:
                return False           
        return True

    # 4 - Fecha Validez presupuesto
    # esta no es necesaria porque en el pedido desbloqueado no se muestra

    # 5 - Precio correcto actualizado
    # Pendiente
    def check_price_update(self):
        self.ensure_one()
        for line in self.order_line:
            if line.order_id.pricelist_id and line.order_id.partner_id:                        
                product = line.product_id.with_context(
                    lang=line.order_id.partner_id.lang,
                    partner=line.order_id.partner_id,
                    quantity=line.product_uom_qty,
                    # date=line.order_id.date_order,
                    date=fields.Datetime.now(),
                    pricelist=line.order_id.pricelist_id.id,
                    uom=line.product_uom.id,
                    fiscal_position=line.env.context.get('fiscal_position')
                )
                precio_unitario_actual = round(self.env['account.tax']._fix_tax_included_price_company(line._get_display_price(product), 
                                                product.taxes_id, line.tax_id, line.company_id),2)

                precio_unitario = round(line.price_unit,2)

                if precio_unitario != precio_unitario_actual and line.qty_invoiced == 0:                
                    return False

        return True
    
    # 6 - Cambio tipo de venta
    def check_sale_type(self):
        self.ensure_one()
        if self.type_id.id != self.partner_id.sale_type.id:
            return False
        return True

    # 7 - En clima
    # No aplica acá

    # 8 - Precio costo mayor a precio de venta
    # 
    def check_cost_price(self):
        self.ensure_one()
        if any(self.order_line.filtered(lambda x: x.purchase_price > x.price_unit 
                                        and x.product_id.type!='service'
                                        and x.qty_invoiced == 0)):
            return False
        return True


class SaleOrder(models.Model):
    _inherit = ['sale.order', 'base.exception']
    _name = 'sale.order'
    # _inherit = 'sale.order'

    unlocked = fields.Boolean("Pedido desbloqueado",default=False,copy=False)

    def detect_exceptions(self):
        # if self.state == 'draft':
        if self.unlocked:
            res = super(SaleOrder, self).detect_exceptions()
            # import pdb; pdb.set_trace()
        else:
            # con esto anulo el comportamiento por defecto del módulo
            # que es que pida autorización al confirmar un presupuesto
            res = False

        return res

    def _fields_trigger_check_exception(self):
        res = super(SaleOrder, self)._fields_trigger_check_exception()
        # addons-OCA/sale-workflow/sale_exception/models/sale.py:52
        # res = ['ignore_exception', 'order_line', 'state']
        # esto es para que chequee las reglas cuando SOLO se cambia el tipo de venta (No se cambia el estado ni una linea)
        return res + ['type_id']

    def sale_check_exception(self):        
        orders = self.filtered(lambda s: s.state == 'sale')
        for rec in orders:
            # import pdb; pdb.set_trace()
            # orders._check_exception()
            if rec.detect_exceptions():
                # import pdb; pdb.set_trace()
                return rec._popup_exceptions()

    def action_done(self):
        for rec in self:
            if rec.detect_exceptions() and not rec.ignore_exception and rec.unlocked:
                raise ValidationError('Debe resolver la excepción antes de poder bloquear el pedido')
        return super().action_done()

    def action_unlock(self):
        for rec in self:
            rec.unlocked = True
            rec.ignore_exception = False
        return super().action_unlock()


    def action_invoice_create(self, grouped=False, final=False):
        for rec in self:
            if rec.detect_exceptions() and not rec.ignore_exception and rec.unlocked:
                raise ValidationError('Debe resolver la excepción antes de poder facturar')

        res = super(SaleOrder, self).action_invoice_create(grouped, final)