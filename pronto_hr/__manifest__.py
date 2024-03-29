# Copyright 2023 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pronto_hr",
    "summary": "Mejoras solicitadas por el cliente",
    "version": "15.0.1.1.0",
    "category": "HR",
    "website": "https://github.com/juanpgarza/pronto-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "hr",
            "announcement", # OCA
        ],
    "data": [
        "data/pronto_hr_data.xml",
        "views/hr_employee_views.xml",
        ],
    "installable": True,
}
