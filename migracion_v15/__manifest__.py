# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Migración a v15",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        ######################################################
        ### CORE CE ###
        ######################################################
        "account",
        "base_automation",
        "crm",
        "l10n_ar",
        "mail",
        "mrp",
        "project",
        "sale_management",
        "sale_stock",
        "stock",
        "website_sale",

        ######################################################
        ### OCA ###
        ######################################################

        # partner-contact
        "base_location",

        # product-atribute
        "product_code_unique",
        "product_dimension",
        "product_pricelist_direct_print",


        #  stock-logistics-workflow
        "stock_no_negative", # INSTALARLO DESPUES DE MIGRAR para que no trabe??
        "stock_picking_back2draft",
        "stock_picking_purchase_order_link",
        "stock_picking_sale_order_link",
        "stock_split_picking",

        # sale-workflow
        "sale_exception",
        "sale_order_line_description",
        "sale_order_type",
        "sale_product_multi_add",
        "sale_stock_picking_note",
        "sale_tier_validation",

        # web
        "web_company_color",
        "web_environment_ribbon",
        "web_refresher",
        "web_remember_tree_column_width",

        ######################################################
        ### adhoc ###
        ######################################################
        # account-payment
        "account_payment_group",

        # product
        "product_ux",

        # sale
        "sale_order_type_ux",
        "sale_ux",

        # stock
        "stock_voucher",


        ######################################################
        ### juanpgarza ###
        ######################################################

        # stock-addons
        "stock_picking_tag",
        "stock_picking_return_reason",
        "stock_picking_return_wait_replacement",

        ],
    "data": [
#        'views/report_payment_group.xml',
        ],
    "installable": True,
    'post_init_hook': 'post_init_hook',
}
