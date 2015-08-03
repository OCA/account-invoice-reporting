# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Ursa Informative Systems (<www.ursainfosystems.com>).
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
###############################################################################

{
    "name": "Interactive Partner Aging",
    "version": "1.7.2",
    "author": 'Ursa Information Systems,'
              'Odoo Community Association (OCA)',
    "summary": "Aging as a view - invoices and credits (Ursa)",
    'website': 'http://www.ursainfosystems.com',
    "category": 'Accounting & Finance',
    "description": """\
Interactive Partner Aging
=========================

This module creates new AR and AP views.

The default OpenERP Aged Partner balance report is a static PDF that is based
on the difference between credits and debits, not based on documents such as
Invoices and Payments. It also does not consider unapplied payments. This
version is interactive and more complete.

A detailed description of this module can be found at
https://github.com/OCA/account-invoice-reporting/raw/7.0/partner_aging/\
partner_aging_README.pdf

Bug Tracker
===========

Bugs are tracked on `GitHub Issues \
<https://github.com/OCA/account-fiscal-rule/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and \
welcomed feedback
`here <https://github.com/OCA/account-invoice-reporting/issues/\
new?body=module:%20partner_aging%0Aversion:%207.0%0A%0A\
**Steps%20to%20reproduce**%0A-%20...%0A%0A\
**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Ursa Information Systems <contact@ursainfosystems.com>
* Guillaume Auger <guillaume.auger@savoirfairelinux.com>
* Loïc Faure-Lacroix <loic.lacroix@savoirfairelinux.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>


Maintainers
-----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
      :target: http://odoo-community.org

      This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission os to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
""",
    "images": [],
    "depends": ["base", "account_accountant"],
    "data": [
        'partner_aging_supplier.xml',
        'partner_aging_customer.xml',
        'security/ir.model.access.csv',
    ],
    "test": [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}
