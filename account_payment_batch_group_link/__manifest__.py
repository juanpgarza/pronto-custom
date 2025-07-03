# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "account_payment_batch_group_link",
    "summary": "Link desde payment batch (v17) a payment group (v15)",
    "version": "17.0.1.0.0",
    "category": "account",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "account_payment_batch_st",
        ],
    "data":
        [
            "views/account_payment_batch_st_views.xml",
            'data/config_parameter.xml',
        ],
    "installable": False,
}
