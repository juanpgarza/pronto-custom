# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_product_ui",
    "summary": "Mejoras a la UI solicitadas por el cliente",
    "version": "15.0.2.0.0",
    "category": "Product",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "product",
        "stock",
        "pronto",
        ],
    'data': [
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/product_family_views.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
