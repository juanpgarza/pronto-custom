# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_report",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "15.0.1.0.0",
    "category": "report",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "sale",
        ],
    "data": [
            # 'security/pronto_stock_security.xml',
            # 'views/stock_picking_views.xml',
            # 'wizard/update_inventory_product_views.xml',
            'security/ir.model.access.csv',
            "report/pronto_sale_report_view.xml",            
        ],
    "installable": True,
}
