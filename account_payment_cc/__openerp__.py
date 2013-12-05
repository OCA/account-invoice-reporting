# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Credit Card Payments",
    "version" : "1.7",
    "category" : "Accounting",
    "author" : 'Ursa & OpenERP SA',
    "summary": "Adds support for Credit Card AP movements. (Ursa)",
    "description": """
Cleaner management of credit card transactions (expenses) by employees
======================================================================

This module provides a way to record Credit Card purchases and to pay them in the same way regular purchases are recorded 
(via Supplier Invoices) and paid (via Supplier Payments). 

Rationale
---------
   
Without this module, if Supplier Invoices are used to record Credit Card purchases, the liability (AP) from the Supplier/Vendor 
must be moved to the Credit Card Company via a Manual Journal Entry.  Because a Journal Entry contains less information than a 
Supplier Invoice, there may be a loss of information that affects book keeping accuracy and the ability to properly reconcile 
the AP amount when the Credit Card statement arrives and needs to be settled.  This method also requires and additional step 
not needed when a Supplier Invoice is paid via bank or cash. 

Without this module, if Manual Journal Entries are used to record Credit Card purchases, there may be a loss of information that 
affects book keeping accuracy and the ability to properly reconcile the AP amount when the Credit Card statement arrives and needs
to be settled. This method also requires a different workflow to the one that is used when a bank or cash payment is made.
 
Details
-------

This module automates the creation of the Manual Journal Entry required to move the AP to the Credit Card Company, retains all 
information about the purchase in an Invoice document, and leverages the standard purchase and payment workflow already in place 
for bank and cash payments. It supports as many Credit Cards as are needed, configured in the same way an additional payment method 
would be (i.e. via the creation of a new Journal). 


To settle a Credit Card statement, the regular workflow to record a Supplier Payment is used allowing the removal of charges not
included in the statement.  Non purchase transactions like fees for annual membership, balance transfers, cash advances and foreign 
transactions; as well as charges for late payments and returned checks; can be entered either as Supplier Invoices or Manual Journal 
Entries as users elect.  Both of these methods will allow these items to be settled when making a payment to the Credit Card Company. 

This module also supports payment cancellation and re-entry (in the case a mistaken amount is entered) as well as refunds (where the 
purchase is returned and a credit from the Credit Card Company will be issued). 
    
    
Developer Notes
---------------
* OpenERP Version:  7.0
* Ursa Dev Team: RC
* OpenERP Dev Team: DS, JA

Contact
-------
* contact@ursainfosystems.com
        """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "images" : [
        'images/one.png',
        'images/two.png',
        'images/three.png',
        'images/four.png',    
        'images/five.png',
    ],
    "depends" : ["account_voucher"],
    "data" : [
        'account_view.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
