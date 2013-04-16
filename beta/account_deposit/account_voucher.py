# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _

class account_voucher(osv.osv):

    _inherit = 'account.voucher'

    _columns = {
        'deferred_revenue': fields.boolean('Record as Deposit', readonly=True, states={'draft':[('readonly',False)]}, help='Check the box if Payment is Unearned Revenue, Deferred Revenue or Advanced Deposit. If Un-Checked the payment is processed as regular receivable, crediting AR.'),
        'unearned_revenue_id': fields.many2one('account.account', 'Receivable Account', readonly=True,states={'draft':[('readonly',False)]}),
    }

    _defaults = {
        'deferred_revenue': True,
    }

    def onchange_deferred_revenue(self, cr, uid, ids, drevenue, partner_id, context=None):
        vals = {'value': {'unearned_revenue_id': False, 'deferred_revenue': drevenue}}
        if not partner_id:
            return {'value': {'unearned_revenue_id': False}}
        if drevenue and partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            if partner.unearned_revenue_id:
                vals['value'].update({'unearned_revenue_id': partner.unearned_revenue_id.id})
            else:
                raise osv.except_osv(_('Warning'), _("No 'Deposit Account' is defined for Customer '%s'.")%(partner.name))
        else:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            if partner.property_account_receivable:
                vals['value'].update({'unearned_revenue_id': partner.property_account_receivable.id})
        return vals

    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, drevenue=True,context=None):
        if not journal_id:
            return False
        journal_pool = self.pool.get('account.journal')
        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        account_id = journal.default_credit_account_id or journal.default_debit_account_id
        tax_id = False
        if account_id and account_id.tax_ids:
            tax_id = account_id.tax_ids[0].id

        vals = self.onchange_price(cr, uid, ids, line_ids, tax_id, partner_id, context)
        vals['value'].update({'tax_id':tax_id,'amount': amount})
        currency_id = False
        if journal.currency:
            currency_id = journal.currency.id
        vals['value'].update({'currency_id': currency_id})
        res = self.onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, drevenue, context)
        for key in res.keys():
            vals[key].update(res[key])
        return vals


    def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, drevenue=True,context=None):
        res = super(account_voucher,self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=context)
        if 'value' not in res:
            res['value'] = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            rec = self.onchange_deferred_revenue(cr, uid, ids, drevenue, partner_id, context=context)
            res['value'].update({'unearned_revenue_id': rec['value']['unearned_revenue_id'], 
                                    'deferred_revenue': drevenue})
        else:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            if partner.property_account_receivable:
                res['value'].update({'unearned_revenue_id': False,
                                     'deferred_revenue': drevenue})
        return res

    def writeoff_move_line_get(self, cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, context=None):
        move_line = super(account_voucher, self).writeoff_move_line_get(cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, context)
        voucher_brw = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
        current_currency_obj = voucher_brw.currency_id or voucher_brw.journal_id.company_id.currency_id
        if not self.pool.get('res.currency').is_zero(cr, uid, current_currency_obj, line_total):
            if voucher_brw.type in ('sale','receipt') and voucher_brw.deferred_revenue:
                account_id = voucher_brw.unearned_revenue_id and voucher_brw.unearned_revenue_id.id or voucher_brw.partner_id.property_account_receivable.id
                move_line.update({'account_id': account_id})
        return move_line

        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
