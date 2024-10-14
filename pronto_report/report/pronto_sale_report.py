# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from psycopg2.extensions import AsIs

class ProntoSaleReport(models.Model):
    _name = "pronto.sale.report"
    _description = "Reporte Ventas Pronto"
    _auto = False
    # _rec_name = "commission_id"

    order_id = fields.Many2one('sale.order', 'Pedido', readonly=True)
    date = fields.Datetime('Fecha de pedido', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Cliente', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Tarifa', readonly=True)
    name = fields.Char('Número de pedido', readonly=True)       
    product_id = fields.Many2one('product.product', 'Producto', readonly=True)    
    # product_tmpl_id = fields.Many2one('product.template', 'Plantilla de producto', readonly=True)
    product_uom_qty = fields.Float('Cant. pedida', readonly=True)
    price_unit = fields.Float('Precio Unitario', readonly=True, group_operator='sum')
    subtotal = fields.Float('Subtotal', readonly=True, group_operator='sum')
    discount = fields.Float('Descuento', readonly=True, group_operator='sum')
    precio_costo_unitario = fields.Float('Precio de costo unitario', readonly=True, group_operator='sum')
    precio_costo_total = fields.Float('Precio de costo total', readonly=True, group_operator='sum')
    margin = fields.Float('Margen', readonly=True)
    margin_percent = fields.Float('% Margen', readonly=True)
    user_id = fields.Many2one('res.users', 'Comercial', readonly=True)
    categ_id = fields.Many2one('product.category', 'Categoría', readonly=True)
    categ_name = fields.Char("Nombre Cat.")
    currency_id = fields.Many2one('res.currency', 'Moneda', readonly=True)
    cotizacion = fields.Float('Cotizacion', readonly=True)
    opportunity_id = fields.Many2one('crm.lead', 'Oportunidad', readonly=True)

    def _select(self):
        select_str = """
            SELECT l.id as id,
            l.order_id as order_id,
            s.date_order as date,
            s.partner_id as partner_id,
            s.pricelist_id as pricelist_id,
            s.name as name,            
            l.product_id as product_id,
            t.uom_id as product_uom,
            l.product_uom_qty as product_uom_qty,
            case when s.currency_id = 2 then price_unit * s.cotizacion else l.price_unit end as price_unit,
            case when s.currency_id = 2 then product_uom_qty * price_unit * s.cotizacion * (1 - l.discount/100) when s.currency_id = 19 then product_uom_qty * price_unit * (1 - l.discount/100) END subtotal,
            l.discount as discount,
            case when s.currency_id = 2 then l.purchase_price * s.cotizacion else l.purchase_price end as precio_costo_unitario,
            case when s.currency_id = 2 then l.purchase_price * s.cotizacion * product_uom_qty else l.purchase_price * product_uom_qty end as precio_costo_total,            
            case when s.currency_id = 2 then l.margin * s.cotizacion else l.margin end as margin,
            l.margin_percent * 100 as margin_percent,            
            s.user_id as user_id,            
            t.categ_id as categ_id,
            pc.name as categ_name,
            s.currency_id as currency_id,
            s.cotizacion as cotizacion,
            s.opportunity_id as opportunity_id

        """
        return select_str

    def _from(self):
        from_str = """
                sale_order_line l
                      join sale_order s on (l.order_id=s.id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join product_category pc on t.categ_id = pc.id
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE
                l.display_type is null
                and s.invoice_status = 'invoiced'
        """

        return where_str
    
    # def _group_by(self):
    #     group_by_str = """
    #         GROUP BY ai.partner_id,
    #         ai.state,
    #         ai.date,
    #         ail.company_id,
    #         rp.id,
    #         pt.categ_id,
    #         ail.product_id,
    #         pt.uom_id,
    #         ail.id,
    #         aila.settled,
    #         aila.commission_id
    #     """
    #     return group_by_str

    @api.model
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            "CREATE or REPLACE VIEW %s AS ( %s FROM ( %s ) %s)",
            (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._from()),
                AsIs(self._where()),
                # AsIs(self._group_by()),
            ),
        )
