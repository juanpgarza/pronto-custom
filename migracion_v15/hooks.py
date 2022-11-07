from odoo import SUPERUSER_ID, api
import logging
_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    Create a payment group for every existint payment
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    # instalar módulos
    # no funciona ?? los pongo a todos en el depends
    # env['ir.module.module'].search([('name','=','project')]).button_immediate_install()

    # activar lang ARG
    lang = env['res.lang'].search([])
    lang._activate_lang('es_AR')

    env.ref('base.ARS').active = True
    env.ref('base.USD').active = True
    env.ref('base.USD').symbol = 'USD'
    env.ref('base.main_company').currency_id = env.ref('base.ARS')

    # cambiar precision decimal de precio de producto
    env['decimal.precision'].search([('name', '=', 'Product Price')]).write({'digits': 4})

    # activar listas de precios
    newSettings = env['res.config.settings'].create({})
    newSettings.update(
                {
                    # sale
                    'group_product_pricelist' : True,
                    'group_sale_pricelist' : True,
                    'product_pricelist_setting': 'advanced',
                    'group_product_variant' : True,
                    'group_uom' : True,
                    'group_discount_per_so_line' : True,
                    'module_sale_margin' : True,
                    'group_sale_order_template' : True,
                    'module_sale_quotation_builder' : True,
                    'group_auto_done_setting' : True,
                    'use_quotation_validity_days' : True,
                    'quotation_validity_days': 2,
                    'module_delivery': True,

                    # website_sale
                    'group_delivery_invoice_address': True,
                    # sale_ux
                    "update_prices_automatically": True,

                    # stock
                    "group_stock_adv_location": True,
                    "group_stock_production_lot": True,
                    "module_stock_barcode": True,
                    "group_stock_packaging": True,
                }
                )
    newSettings.execute()




