# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    'name' : 'Customer Deposits',
    'version' : '1.7',
    "author" : 'Ursa & OpenERP SA',
    'summary': 'Add support for payments as liabilities (Ursa)',
    'description': """
This module supports the recording of advanced customer deposits.  These occur when a vendor receives money from their customer before a service is provided or shipment of goods is made.  These funds are liabilities due to the fact that if the performance of the sale is not completed the customer would want a refund of their deposit because they have received nothing.  

These types of transactions are commonly referred to as Unearned Revenue, Unearned Income and Deferred Revenue.  They should be shown in the liability section of the balance sheet.  No revenue (profit & loss statement) effect should occur until the revenue has been earned.  When the revenue has been earned (shipment of goods or services performed) the liability is removed and the revenue is recognized.  As these deposits are received they need to be specifically tracked by who made it so they may be applied against their open AR balances.

A detailed description of this module can be found at https://launchpad.net/openerp-shared/7.0/stable/+download/account_deposit_README.pdf

OpenERP Version:  7.0
Ursa Dev Team: RC
OpenERP Dev Team: DS, JA

Contact: contact@ursainfosystems.com
        """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    "category": 'Accounting & Finance',
    "images" : [],
    "depends" : ["account_voucher"],
    'data' : [
        'res_partner_view.xml',
        'account_voucher_view.xml',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
