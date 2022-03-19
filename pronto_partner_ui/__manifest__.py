# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_partner_ui",
    "summary": "Mejoras a la UI solicitadas por el cliente",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "category": "Partner",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "depends": [
        "base",
        "product",
        "sale_order_type",
        ],
    "data": [
        'security/security_data.xml',
        'views/res_partner_views.xml',
        ],
    "installable": True,
}
