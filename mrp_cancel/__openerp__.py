# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Single step MO Cancel",
    "version" : "1.7",
    "author" : "Ursa Information Systems",
    "summary": "For MO's with the picking not completed, cancel the picking and the MO in one step.",
    'description':
        """
By default, an MO cannot be cancelled unless the associated picking is also cancelled.  This module cancels the picking (if it has not been processed) and the MO in a single step.  All MO related stock moves are cancelled and Stock levels are as you would expect them to be if the MO never existed.  

OpenERP Version:  7.0
Ursa Dev Team: RC

Contact: contact@ursainfosystems.com
        """,
    'author': 'Ursa Information Systems',
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category" : "Manufacturing",
    "depends" : ["base", "mrp", "stock"],
    "installable": True,
    "active": True
}
