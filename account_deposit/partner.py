# -*- coding: utf-8 -*-
from openerp.osv import fields, orm


class res_partner(orm.Model):

    _inherit = 'res.partner'

    _columns = {
        'unearned_revenue_id': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Deposit Account",
            view_load=True,
            domain="[('type', '=', 'receivable')]",
            help=(
                "This account will be used instead of the default one as "
                "the receivable account for payments processed as deposits"
            ),
            required=True
        ),
    }
