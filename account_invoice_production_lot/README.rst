.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
Invoice Production Lots
=======================

This module shows, for each (customer) invoice line, the delivered production
lots.

Configuration
=============

* Go to **Inventory > Configuration > Settings**, and activate option "Track
  lots or serial numbers" in order to manage lots in your instance.
* Go to **Sales > Sales > Products** and select or create a product and check
  that product has enabled its tracking by lots in **Inventory** tab.

Usage
=====

* Create a sales order.
* When the sales order is accepted and delivery order created,
  process picking list setting serial numbers on delivered lines.
* Create the invoice, and the serial numbers are displayed in the "Production
  Lots" on invoice line form (if visible) and in "formatted note" field on
  invoice report.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/94/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-invoice-reporting/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smash it by providing detailed and welcomed
feedback.

Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Alessio Gerace <alessio.gerace@agilebg.com>
* Vicent Cubells <vicent.cubells@tecnativa.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
