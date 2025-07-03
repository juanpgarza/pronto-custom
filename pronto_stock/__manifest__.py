# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_stock",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "17.0.1.0.1",
    "category": "Stock",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "stock",
            "sale_stock", # CORE. por el campo sale_id de stock.picking
            "stock_picking_invoice_link",
            "stock_inventory",
            "stock_picking_tag",
            "stock_picking_state_assigned",
            "stock_voucher", # adhoc --> para valor declarado
        ],
    "data": [
            'security/pronto_stock_security.xml',
            'views/stock_picking_views.xml',
            'wizard/update_inventory_product_views.xml',
            'security/ir.model.access.csv',
            'views/report_customer_delivery_views.xml',
            'wizard/report_customer_delivery_wizard_views.xml',
        ],
    "installable": False,
}
