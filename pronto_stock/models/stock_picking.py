from odoo import models, api, fields
from odoo.exceptions import ValidationError

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