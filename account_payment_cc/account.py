# -*- coding: utf-8 -*-
from openerp.osv import fields, orm


class account_journal(orm.Model):
    _inherit = "account.journal"

    _columns = {
        'support_creditcard_transactions': fields.boolean(
            'Transfer AP to Credit Card Company',
        ),
        'partner_id': fields.many2one(
            'res.partner',
            'Credit Card Company'
        ),
    }
