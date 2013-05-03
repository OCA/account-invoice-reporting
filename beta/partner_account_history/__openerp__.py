# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Partner Financial History",
    "version" : "1.7",
    "author" : 'Ursa Information Systems',
    "summary": "Adds a new view of all financial transactions (Ursa)",
    "description" : """
This module creates a Financial History view for every Partner.

A detailed description of this module can be found at https://launchpad.net/openerp-shared/7.0/stable/+download/partner_account_history_README.pdf

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
        'partner_account_history_view.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


