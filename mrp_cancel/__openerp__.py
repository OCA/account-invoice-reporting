﻿# -*- coding: utf-8 -*-

{
    "name": "Cancel Manufacturing Orders",
    "version": "1.7",
    "category": "Manufacturing",
    "author": "Ursa Information Systems",
    "summary": "Cancel MO's in a single step (Ursa)",
    "description": """
One less step when cancelling a Manufacturing Order
===================================================

By default, an MO cannot be cancelled unless the associated picking is also
cancelled.  This module cancels the picking (if it has not been processed) and
the MO in a single step.  All MO related stock moves are cancelled and Stock
levels are as you would expect them to be if the MO never existed.

A detailed description of this module can be found at
https://launchpad.net/openerp-shared/7.0/stable/+download/mrp_cancel_README.pdf

Developer Notes
---------------
* OpenERP Version:  7.0
* Ursa Dev Team: RC


Contact
-------
* contact@ursainfosystems.com
    """,
    "maintainer": 'Ursa Information Systems',
    "website": 'http://www.ursainfosystems.com',
    "depends": [
        "base",
        "mrp",
        "stock",
    ],
    "init_xml": [],
    "demo_xml": [],
    "data": [
    ],
    "test": [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}
