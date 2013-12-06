# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import fields, osv

class account_journal(osv.osv):
    _inherit = "account.journal"

    _columns = {
        'support_creditcard_transactions': fields.boolean('Transfer AP to Credit Card Company',),
        'partner_id': fields.many2one('res.partner','Credit Card Company'),
    }

    _defaults = {
    
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
