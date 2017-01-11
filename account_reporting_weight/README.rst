.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Weights in the invoices analysis view
=====================================

This module adds the measure "Weight" in the invoices analysis view. This is
caught from 2 possible sources:

* If the UoM of the product is one of the category "Weight", the value is taken
  from the ordered quantity.
* If the UoM of the product is another, then the weight is taken from the
  weight field of the product multiply by the ordered quantity.

Configuration
=============

You need to be at least "Accountant" on "Accounting & Finance" role for
seeing the report.

Usage
=====

#. Go to *Invoicing > Reporting > Businness Intelligence > Invoices*.
#. Add the "Weight" measure from your "Measures" dropdown in your analysis.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/94/9.0

Known issues / Roadmap
======================

* The weight quantity is expressed in the unit of measure of the product,
  so if you have several weight UoMs across your products, the global sum won't
  make sense.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>

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
