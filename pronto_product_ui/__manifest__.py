# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_product_ui",
    "summary": "Mejoras a la UI solicitadas por el cliente",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "category": "Product",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "depends": [
        "product",
        "stock",
        ],
    "data": [
        'security/security_data.xml',
        'views/product_template_views.xml',
        ],
    "installable": True,
}
