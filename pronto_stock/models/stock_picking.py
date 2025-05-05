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

    # sobre-escribo el metodo de stock_voucher (adhoc) para calculo de valor declarado
    # cambio: price_reduce_taxexcl por purchase_price
    # CUIDADO! siempre verificar que funcione bien con pedidos en pesos y en dolares
    # si el costo lo saco de order_line.product_id.standard_price NO FUNCIONA cuando la lista es en Dolares
    # porque esta en pesos y despues lo pasa a dolares
    @api.depends(
        'automatic_declare_value',
        'move_ids.state',
        'move_ids.quantity',
    )
    def _compute_declared_value(self):
        for rec in self.filtered(lambda p: p.automatic_declare_value and p.state not in ['done', 'cancel']):
            import pdb; pdb.set_trace()
            done_value = 0.0
            picking_value = 0.0
            inmediate_transfer = True
            pricelist = False
            stock_bom_lines = self.env['stock.move']
            for move_line in rec.move_ids.filtered(
                    lambda x: x.state != 'cancel'):
                order_line = move_line.sale_line_id
                if move_line.quantity:
                    inmediate_transfer = False
                if order_line:
                    pricelist = rec.sale_id.pricelist_id
                    # this should happends only if on SO it's a bom kit
                    if not order_line.product_id == move_line.product_id:
                        stock_bom_lines |= move_line
                        continue
                    so_product_qty = move_line.product_uom_qty
                    so_qty_done = move_line.quantity
                    # convert quantities if move line uom and sale line uom
                    # are different
                    if move_line.product_uom != order_line.product_uom:
                        so_product_qty = \
                            move_line.product_uom._compute_quantity(
                                move_line.product_uom_qty,
                                order_line.product_uom)
                        so_qty_done = \
                            move_line.product_uom._compute_quantity(
                                move_line.quantity,
                                order_line.product_uom)
                    picking_value += (order_line.purchase_price *
                                      so_product_qty)
                    done_value += (order_line.purchase_price *
                                   so_qty_done)
                elif rec.picking_type_id.pricelist_id:
                    pricelist = rec.picking_type_id.pricelist_id
                    price = rec.picking_type_id.pricelist_id.with_context(
                        uom=move_line.product_uom.id)._price_get(
                        move_line.product_id,
                        move_line.quantity or 1.0,
                        partner=rec.partner_id.id)[
                        rec.picking_type_id.pricelist_id.id]
                    picking_value += (price * move_line.product_uom_qty)
                    done_value += (price * move_line.quantity)

            # This is for product in a kit (should only happen if sale_mrp ins
            # installed). If it is bom we only compute amount if all bom
            # components are deliverd (same as in bom _get_delivered_qty)
            bom_enable = 'bom_ids' in self.env['product.template']._fields
            if bom_enable:
                for so_bom_line in stock_bom_lines.mapped('sale_line_id'):
                    bom = self.env["mrp.bom"]._bom_find(products = so_bom_line.product_id)[so_bom_line.product_id]
                    if bom and bom.type == 'phantom':
                        bom_moves = so_bom_line.move_ids & stock_bom_lines
                        done_avg = []
                        picking_avg = []
                        boms, lines = bom.sudo().explode(
                            so_bom_line.product_id,
                            so_bom_line.product_uom_qty,
                            picking_type=bom.picking_type_id)
                        for move in bom_moves:
                            bom_quantity = 0.0
                            for bom_line, line_data in lines:
                                if bom_line.product_id == move.product_id:
                                    bom_quantity += line_data['qty']
                            if not bom_quantity:
                                continue
                            picking_avg.append((
                                move.product_uom_qty / bom_quantity))
                            done_avg.append(
                                (move.quantity / bom_quantity))
                        picking_value += so_bom_line.price_reduce_taxexcl * (
                            sum(picking_avg) / len(picking_avg))
                        done_value += so_bom_line.price_reduce_taxexcl * (
                            sum(done_avg) / len(done_avg))

            declared_value = picking_value if inmediate_transfer\
                else done_value
            if pricelist:
                # we convert the declared_value to the currency of the company
                rec.declared_value = pricelist.currency_id._convert(
                    declared_value, rec.company_id.currency_id, rec.company_id,
                    rec.sale_id.date_order or fields.Date.today())
            else:
                rec.declared_value = declared_value