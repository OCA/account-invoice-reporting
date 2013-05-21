# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    'name': 'Partner Days to Pay',
    'version': '1.7',
	'author': 'Ursa Information Systems',
	'summary': 'Adds receivables and payables statistics to partners (Ursa)',
	'description': """
This module displays statistics related to the receivables and payables behavior of a partner on the Accounting tab of the partner form view.

A detailed description of this module can be found at https://launchpad.net/openerp-shared/7.0/stable/+download/partner_dtp_README.pdf

OpenERP Version:  7.0
Ursa Dev Team: RC

Contact: contact@ursainfosystems.com
        """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category": 'Accounting & Finance',
    "images" : [],
    'depends': ['base','account'],
    'data' : [
        'res_partner_view.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
