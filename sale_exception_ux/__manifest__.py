# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "sale_exception_ux",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/juanpgarza/sale-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "sale_exception",
            "sale_order_type",
        ],
    "data": [
        'data/exception_rule_data.xml',
        'views/sale_order_views.xml',
        ],
    "installable": True,
}
