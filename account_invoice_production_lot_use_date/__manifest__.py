# -*- coding: utf-8 -*-
# Copyright 2018 Nicola Malcontenti <nicola.malcontenti@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Invoice Production Lot Use Date",
    "version": "10.0.1.1.0",
    "author": "Agile Business Group,"
              "Odoo Community Association (OCA)",
    "summary": "Display delivered end date for lots in invoice report",
    'website': 'https://github.com/OCA/account-invoice-reporting',
    'license': 'AGPL-3',
    'category': 'Accounting & Finance',
    "depends": [
        "account_invoice_production_lot",
        "product_expiry"
    ],
    'data': [],
    'installable': True,
}
