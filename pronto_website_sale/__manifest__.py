# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_website_sale",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "website_sale",
            "product_sale_additional_description",
        ],
    "data": [
            # 'security/pronto_sale_security.xml',
            'views/website_sale_template.xml',
        ],
    "installable": True,
}
