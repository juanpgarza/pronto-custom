# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Migración a v15",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        ######################################################
        ### CORE CE ###
        ######################################################
        "account",
        "base_automation",
        "crm",
        "l10n_ar",
        "mail",
        "mrp",
        "project",
        "sale_management",
        "sale_stock",
        "stock",
        "website_sale",

        ######################################################
        ### OCA ###
        ######################################################

        # account-invoicing
        "account_move_tier_validation",

        # account-financial-tools
        "account_balance_line",
        "account_usability",

        # account-financial-reporting
        "account_financial_report",
        "partner_statement",

        # account-payment
        "account_due_list",
        "partner_aging",

        # bank-payment
        "account_payment_mode",
        "account_payment_partner",
        "account_payment_purchase",
        "account_payment_sale",

        # commission
        "commission",
        "commission_formula",
        "sale_commission",

        # credit-control
        "account_credit_control",
        "account_financial_risk",
        "sale_financial_risk",

        # partner-contact
        "base_location",

        # product-atribute
        "product_code_unique",
        "product_dimension",
        "product_pricelist_direct_print",

        # purchase-workflow
        "purchase_discount",
        "purchase_tier_validation",

        #  stock-logistics-warehouse
        "stock_change_qty_reason",
        "stock_quant_manual_assign",

        #  stock-logistics-workflow
        "stock_no_negative", # INSTALARLO DESPUES DE MIGRAR para que no trabe??
        "stock_picking_back2draft",
        "stock_picking_invoice_link",
        "stock_picking_purchase_order_link",
        "stock_picking_sale_order_link",
        "stock_split_picking",

        # sale-reporting
        "sale_report_margin",

        # sale-workflow
        "sale_exception",
        "sale_order_line_description",
        "sale_order_type",
        "sale_product_multi_add",
        "sale_stock_picking_note",
        "sale_tier_validation",

        # server-ux
        "base_optional_quick_create",
        "base_tier_validation",
        "base_tier_validation_formula",
        "date_range",
        "mass_editing",

        # server-tools
        # "base_exception", se auto-instala, es dependencia de otro módulo

        # social
        "mail_activity_board",
        "mail_activity_partner",
        "mail_attach_existing_attachment",
# mail_attach_existing_attachment_account
        "mass_mailing_partner",


        # web
        "web_company_color",
        "web_environment_ribbon",
        # "web_ir_actions_act_multi", se auto-instala, es dependencia de otro módulo
        "web_refresher",
        "web_remember_tree_column_width",

        ######################################################
        ### adhoc ###
        ######################################################
        # account-financial-tools


        # account-payment
        "account_payment_group",

        # product
        "product_ux",

        # sale
        "sale_order_type_ux",
        "sale_ux",

        # stock
        "stock_voucher",


        ######################################################
        ### juanpgarza ###
        ######################################################

        # stock-addons
        "stock_picking_tag",
        "stock_picking_return_reason",
        "stock_picking_return_wait_replacement",

        ],
    "data": [
#        'views/report_payment_group.xml',
        ],
    "installable": True,
    'post_init_hook': 'post_init_hook',
}
