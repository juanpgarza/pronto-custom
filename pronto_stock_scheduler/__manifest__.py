# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_stock_scheduler",
    "summary": "Sistema de reserva de stock de Pronto",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "category": "Stock",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "depends": [
        "stock",
        "sale",
        ],
    "data": [
        'views/res_company_views.xml',
        'views/stock_location_views.xml',
        'data/config_parameter.xml',
        'data/mail_activity_type.xml',
        ],
    "installable": True,
}
