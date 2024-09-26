from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_invoice_ids = fields.Many2many(
                comodel_name="account.move", 
                string="Facturas del pedido", 
                compute='_compute_sale_invoice_ids',
    )

    def action_cancel(self):        
        for rec in self.filtered(lambda x: x.state != 'cancel'):
            group = "pronto_stock.group_cancel_picking"
            if not rec.user_has_groups(group):
                group_id = self.env.ref(group)
                raise ValidationError("Opción habilitada solo para los miembros del grupo: \n\n'{} / {}'".format(group_id.sudo().category_id.name,group_id.name))
        return super(StockPicking, self).action_cancel()
    
    def _compute_sale_invoice_ids(self):
        for rec in self:
            # facturas asociadas con el pedido relacionado con la entrega
            rec.sale_invoice_ids = rec.sale_id.mapped('order_line.invoice_lines.move_id').filtered(lambda x: x.move_type == 'out_invoice')

    # src/addons/stock/models/stock_picking.py:420
    # con esto evito que se oculte el tipo de operación EN TODAS LAS SITUACIONES
    def _compute_hide_pickign_type(self):
        super(StockPicking,self)._compute_hide_pickign_type()
        self.hide_picking_type = False

    def _dias_atraso(self):
        return (datetime.now().date() - self.scheduled_date.date()).days
    
    @api.model
    def entregas_atrasadas(self, dias_atraso = 0):
        # self.env['stock.picking'].entregas_atrasadas()
        return self.search([]).filtered(lambda x: x.state not in ('draft', 'done', 'cancel') 
                                        and x.picking_type_id.code == 'outgoing'
                                        and x._dias_atraso() > dias_atraso)

    def _check_product(self, product, qty=1.0):
        res = super(StockPicking, self).action_cancel(product,qty)
        raise ValidationError("OK")
        # return super(StockPicking, self).action_cancel(product,qty)