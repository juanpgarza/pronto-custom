# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_account_cashbox",
    "summary": "",
    "version": "15.0.3.3.0",
    "category": "Accounting",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "account", # core    
        "account_cashbox", # adhoc
        "account_payment_group", # adhoc
        "hr_expense", # core
        ],
    "data": [
            'security/security.xml',
            'views/account_cashbox_cancel_views.xml',
            'wizard/account_cashbox_bank_transfer_wizard.xml',
            'views/account_cashbox_session_line_transaction_views.xml',
            'views/account_cashbox_session_views.xml',
            'views/account_payment_views.xml',
            'views/account_cashbox_views.xml',
            'views/account_cashbox_session_report.xml',
            'data/pronto_account_cashbox_data.xml',
            'wizard/account_cashbox_expense_wizard.xml',
            'security/ir.model.access.csv',
            'views/hr_expense_views.xml',
            'views/account_cashbox_payment_reason_views.xml',
            'wizard/account_cashbox_transfer_wizard.xml',
            'views/account_cashbox_transfer_views.xml',
            'wizard/account_cashbox_transfer_receive_wizard.xml',
            'wizard/account_cashbox_move_wizard.xml',
            'wizard/account_cashbox_supplier_bill_wizard.xml',
            'wizard/account_payment_cancel_wizard.xml',
        ],
    "installable": True,
}
