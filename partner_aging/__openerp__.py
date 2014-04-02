# -*- coding: utf-8 -*-
######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Interactive Partner Aging",
    "version" : "1.7",
    "author" : 'Ursa Information Systems',
    "summary": "Aging as a view - invoices and credits (Ursa)",
    "description" : """
This module creates new AR and AP views.

The default OpenERP Aged Partner balance report is a static PDF that is based on the difference between credits and debits, not based on documents such as Invoices and Payments.  It also does not consider unapplied payments.  This version is interactive and more complete.

A detailed description of this module can be found at https://launchpad.net/openerp-shared/7.0/stable/+download/partner_aging_README.pdf

OpenERP Version:  7.0
Ursa Dev Team: RC

Contact: contact@ursainfosystems.com
""",
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category": 'Accounting & Finance',
    "images" : [],
    "depends" : ["base","account_accountant"],
    "data" : [
              'partner_aging_supplier.xml',
              'partner_aging_customer.xml',
              'security/ir.model.access.csv',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

