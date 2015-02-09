# -*- coding: utf-8 -*-
######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Interactive Partner Aging",
    "version" : "1.8.0",
    "author" : 'Ursa Information Systems',
    "summary": "Aging as a view - invoices and credits (Ursa)",
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

