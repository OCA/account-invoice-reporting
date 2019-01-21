# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Company invoice note",
    'summary': """
        This module add a note field on the company who'll be printed on every
        invoice reports.""",
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': "https://github.com/OCA/account-invoice-reporting",
    'category': 'account',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'document',
    ],
    'data': [
        'views/account_config_settings.xml',
        'reports/report_invoice_document.xml'
    ]
}
