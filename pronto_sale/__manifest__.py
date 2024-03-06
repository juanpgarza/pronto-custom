# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_sale",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "15.0.1.1.0",
    "category": "Sale",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "sale",
            "sale_management",
            "sale_coupon",
        ],
    "data": [
            'security/pronto_sale_security.xml',
            'views/sale_order_views.xml',
        ],
    "installable": True,
}
