# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Partner Deliveries and Invoices",
    "version" : "1.7",
    "category" : "Sales",
    "author" : "Ursa Information Systems",
    "summary": "Quick access to Deliveries and Invoices (Ursa)",
    "description":
        """
New buttons to access linked Deliveries and Invoices
===================================================+

        This module enhances the user experience, making it easier to reference related documents directly from the partner form view.

A detailed description of this module can be found at https://launchpad.net/openerp-shared/7.0/stable/+download/partner_buttons_README.pdf

Developer Notes
---------------
* OpenERP Version:  7.0
* Ursa Dev Team: AO


Contact
-------
* contact@ursainfosystems.com
        """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    'depends' : [
                    'base',
                    'account',
                    'crm',
                    'sale',
                    'stock'
                ],
    'init_xml': [],
    'data':[
        'crm_view.xml',
            ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: