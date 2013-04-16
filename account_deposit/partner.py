# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import osv
from openerp.osv import fields

class res_partner(osv.osv):

    _inherit = 'res.partner'

    _columns = {
        'unearned_revenue_id': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Deposit Account",
            view_load=True,
            domain="[('type', '=', 'receivable')]",
            help="This account will be used instead of the default one as the receivable account for payments processed as deposits",
            required=True),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
