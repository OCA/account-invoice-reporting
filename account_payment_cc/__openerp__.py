# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Credit Card Payments",
    "version" : "1.7",
    "author" : 'Ursa & OpenERP SA',
    "summary": "Adds support for Credit Card AP movements.",
    "description": """
This module supports the entry of credit card transactions as Supplier Invoices, with payments moving the AP from the vendor to the credit card company.  A single Supplier Payment can then be made when a credit card statement needs to be paid.  New options on the Journal allow for this.  The workflows for recording and paying vendor purchases remain the same, so that credit card purchases can be recorded just be using a different Journal.  Multiple Credit Card companies are supported.

A detailed description of this module can be found at https://launchpad.net/openerp-shared/7.0/stable/+download/account_payment_cc_README.pdf

OpenERP Version:  7.0
Ursa Dev Team: RC
OpenERP Dev Team: DS, JA

Contact: contact@ursainfosystems.com
        """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category": 'Accounting & Finance',
    "images" : [],
    "depends" : ["account_voucher"],
    "data" : [
        'account_view.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
