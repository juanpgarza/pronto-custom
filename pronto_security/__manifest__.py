# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_security",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "15.0.2.0.0",
    "category": "Sale",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "sale",
            "pronto",
        ],
    "data": [
            'security/pronto_security.xml',
            'security/ir.model.access.csv',
            'views/sale_order_views.xml',            
        ],
    "installable": True,
}
