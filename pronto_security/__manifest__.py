# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_security",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "17.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "sale",
            "pronto",
            "stock_inventory",
        ],
    "data": [
            'security/pronto_security.xml',
            'security/ir.model.access.csv',
            'views/sale_order_views.xml',            
        ],
    "installable": False,
}
