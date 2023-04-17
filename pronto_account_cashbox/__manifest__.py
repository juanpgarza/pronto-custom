# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_account_cashbox",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "Accounting",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "account", # core    
        "account_cashbox", # adhoc
        ],
    "data": [
            'views/account_cashbox_session_views.xml',
            'views/account_payment_views.xml',
            'views/account_cashbox_views.xml',
            'views/account_cashbox_session_report.xml',
            'data/pronto_account_cashbox_data.xml',
        ],
    "installable": True,
}
