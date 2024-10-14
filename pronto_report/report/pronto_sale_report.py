# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from psycopg2.extensions import AsIs

class ProntoSaleReport(models.Model):
    _name = "pronto.sale.report"
    _description = "Reporte Ventas Pronto"
    _auto = False
    # _rec_name = "commission_id"

    name = fields.Char('Número de pedido', readonly=True)
    date = fields.Datetime('Fecha de pedido', readonly=True)
    product_id = fields.Many2one('product.product', 'Producto', readonly=True)
    product_uom_qty = fields.Float('Cant. pedida', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Plantilla de producto', readonly=True)
    categ_id = fields.Many2one('product.category', 'Categoría', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Tarifa', readonly=True)


    def _select(self):
        select_str = """
            SELECT l.id as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            l.product_uom_qty as product_uom_qty,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.company_id as company_id,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id
        """
        return select_str

    def _from(self):
        from_str = """
                sale_order_line l
                      join sale_order s on (l.order_id=s.id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
        """
        return from_str

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
            "CREATE or REPLACE VIEW %s AS ( %s FROM ( %s ) )",
            (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._from()),
                # AsIs(self._group_by()),
            ),
        )
