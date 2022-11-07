# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Migración a v15",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "",
    "website": "https://github.com/juanpgarza/zuain-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "account",
        "mail",
        "product_ux",
        "project",
        "crm",
        "sale_management",
        "sale_order_type_ux",
        "sale_ux",
        "stock_voucher",
        "sale_stock",
        "stock",
        "l10n_ar",
        "mrp",
        "website_sale",

        ### OCA ###
        # web
        "web_company_color",
        "web_environment_ribbon",
        "web_refresher",
        "web_remember_tree_column_width",


        ],
    "data": [
#        'views/report_payment_group.xml',
        ],
    "installable": True,
    'post_init_hook': 'post_init_hook',
}
