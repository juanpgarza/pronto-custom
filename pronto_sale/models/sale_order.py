from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fecha_compromiso_vencida = fields.Boolean(string = 'Fecha de Compromiso Vencida', compute = '_compute_vencida', search = '_search_vencida')

    tiene_promociones = fields.Boolean(string="Tiene promociones para aplicar", compute = '_compute_promociones')

    def _compute_promociones(self):
        for rec in self:
            if rec._get_applicable_no_code_promo_program():
            # if rec.no_code_promo_program_ids:
            # if rec._get_applied_programs():
                rec.tiene_promociones = True
            else:
                rec.tiene_promociones = False

    def _compute_vencida(self):
        now = fields.Datetime.now()
        # import pdb; pdb.set_trace()
        for rec in self:
            if rec.state in ('sale','done') and rec.delivery_status == 'to deliver' and rec.commitment_date:
                rec.fecha_compromiso_vencida = now > rec.commitment_date
            else:
                rec.fecha_compromiso_vencida = False
            
    def _search_vencida(self, operator, value):
        now = fields.Datetime.now()
        # import pdb; pdb.set_trace()
        facturas = self.env['sale.order'].search([])        
        ids = facturas.filtered(lambda x: x.state in ('sale','done') and x.delivery_status == 'to deliver' and x.commitment_date and now > x.commitment_date).mapped('id')
        return [('id', 'in', ids)]

    @api.model
    def pedidos_fecha_compromiso_vencida(self):
        res = self.search([('fecha_compromiso_vencida','=',True)])
        # import pdb; pdb.set_trace()
        # len(self.env['sale.order'].pedidos_fecha_compromiso_vencida())
        return res
    
    def action_cancel(self):        
        # solo para pedidos de venta. NO incluye presupuestos
        for rec in self.filtered(lambda x:x.state in ('done','sale') and x.state != 'cancel'):
            group = "pronto_sale.group_cancel_sale_order"
            if not rec.user_has_groups(group):
                group_id = self.env.ref(group)
                raise ValidationError("Opción habilitada solo para los miembros del grupo: \n\n'{} / {}'".format(group_id.sudo().category_id.name,group_id.name))
        return super(SaleOrder, self).action_cancel()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        # Tarea #974
        # Se anula la funcion que hace que tome el comercial asignado al cliente
        # Lo informan a mano         
        user_id = self.user_id
        res = super(SaleOrder, self).onchange_partner_id()
        self.update({'user_id': user_id.id})
        return res

    @api.model
    def default_get(self, fields):
        rec = super(SaleOrder, self).default_get(fields)

        rec['sale_order_template_id'] = False

        return rec

    def _get_reward_values_percentage_amount(self, program):
        # Invalidate multiline fixed_price discount line as they should apply after % discount
        fixed_price_products = self._get_applied_programs().filtered(
            lambda p: p.discount_type == 'fixed_amount'
        ).mapped('discount_line_product_id')
        self.order_line.filtered(lambda l: l.product_id in fixed_price_products).write({'price_unit': 0})

        reward_dict = {}
        lines = self._get_paid_order_lines()
        amount_total = sum([any(line.tax_id.mapped('price_include')) and line.price_total or line.price_subtotal
                            for line in self._get_base_order_lines(program)])
        if program.discount_apply_on == 'cheapest_product':
            line = self._get_cheapest_line()
            if line:
                discount_line_amount = min(line.price_reduce * (program.discount_percentage / 100), amount_total)
                if discount_line_amount:
                    taxes = self.fiscal_position_id.map_tax(line.tax_id)

                    reward_dict[line.tax_id] = {
                        'name': _("Discount: %s", program.name),
                        'product_id': program.discount_line_product_id.id,
                        'price_unit': - discount_line_amount if discount_line_amount > 0 else 0,
                        'product_uom_qty': 1.0,
                        'product_uom': program.discount_line_product_id.uom_id.id,
                        'is_reward_line': True,
                        'tax_id': [(4, tax.id, False) for tax in taxes],
                    }
        elif program.discount_apply_on in ['specific_products', 'on_order']:
            if program.discount_apply_on == 'specific_products':
                # We should not exclude reward line that offer this product since we need to offer only the discount on the real paid product (regular product - free product)
                free_product_lines = self.env['coupon.program'].search([('reward_type', '=', 'product'), ('reward_product_id', 'in', program.discount_specific_product_ids.ids)]).mapped('discount_line_product_id')
                lines = lines.filtered(lambda x: x.product_id in (program.discount_specific_product_ids | free_product_lines))

            # when processing lines we should not discount more than the order remaining total
            currently_discounted_amount = 0
            for line in lines:
                discount_line_amount = min(self._get_reward_values_discount_percentage_per_line(program, line), amount_total - currently_discounted_amount)

                if discount_line_amount:

                    if line.tax_id in reward_dict:
                        reward_dict[line.tax_id]['price_unit'] -= discount_line_amount
                    else:
                        taxes = self.fiscal_position_id.map_tax(line.tax_id)

                        reward_dict[line.tax_id] = {
                            # CUIDADO!! me toma la descrip de venta en ingles!!
                            'name': program.discount_line_product_id.description_sale,

                            'product_id': program.discount_line_product_id.id,
                            'price_unit': - discount_line_amount if discount_line_amount > 0 else 0,
                            'product_uom_qty': 1.0,
                            'product_uom': program.discount_line_product_id.uom_id.id,
                            'is_reward_line': True,
                            'tax_id': [(4, tax.id, False) for tax in taxes],
                        }
                        currently_discounted_amount += discount_line_amount
        # If there is a max amount for discount, we might have to limit some discount lines or completely remove some lines
        max_amount = program._compute_program_amount('discount_max_amount', self.currency_id)
        if max_amount > 0:
            amount_already_given = 0
            for val in list(reward_dict):
                amount_to_discount = amount_already_given + reward_dict[val]["price_unit"]
                if abs(amount_to_discount) > max_amount:
                    reward_dict[val]["price_unit"] = - (max_amount - abs(amount_already_given))
                    add_name = formatLang(self.env, max_amount, currency_obj=self.currency_id)
                    reward_dict[val]["name"] += "( " + _("limited to ") + add_name + ")"
                amount_already_given += reward_dict[val]["price_unit"]
                if reward_dict[val]["price_unit"] == 0:
                    del reward_dict[val]
        return reward_dict.values()