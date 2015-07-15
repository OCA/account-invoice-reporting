# -*- coding: utf-8 -*-
#
#
#    Authors: Jordi Ballester
#    Copyright 2015 Eficent
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#


{
    "name": "Invoices Analysis by invoice number",
    "version": "0.1",
    "depends": ['account'],
    "author": "Eficent,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    'description': """
Invoices Analysis by invoice number
===================================

This module is meant to extend the report 'Invoices Analysis' adding the
invoice internal number, the supplier invoice number and the journal entry.
This is useful to allow the user to drill down.

Usage
=====

Go to 'Reporting | Accounting | Invoices Analysis'.


Known issues / Roadmap
======================

Credits
=======

Contributors
------------
* Jordi Ballester <jordi.ballester@eficent.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

    """,
    "installable": True,
    "data": ["report/account_invoice_report_view.xml"],
    "test": [],
}
