# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import fields, osv
import tools

class partner_aging_supplier(osv.osv):
  
    _name = 'partner.aging.supplier'
    _auto = False

    def invopen(self, cr, uid, ids, context=None):
        """
        @author       Ursa Information Systems
        @description  Create link to view each listed invoice
        """
        models = self.pool.get('ir.model.data')
        view = models.get_object_reference(cr, uid, 'account', 'invoice_form')
        view_id = view and view[1] or False
        
        if not context: 
            context = {} 
        active_id  = context.get('active_id') 
        inv_id = self.browse(cr, uid, ids[0]).invoice_id.id 
   
        print active_id
        print inv_id

        
        return {
            'name': ('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_id,
        }

    _columns = {
        'partner_id': fields.many2one('res.partner', u'Partner',readonly=True),
        'partner_name': fields.text('Name',readonly=True),
        'max_days_overdue': fields.integer(u'Days Overdue',readonly=True),
        'avg_days_overdue': fields.integer(u'Avg Days Overdue',readonly=True),
        'oldest_invoice_date': fields.date(u'Invoice Date',readonly=True),
        'date_due': fields.date(u'Due Date',readonly=True),
        'total': fields.float(u'Total',readonly=True),
        'current': fields.float(u'Current',readonly=True),
        'days_due_01to30': fields.float(u'01/30',readonly=True),
        'days_due_31to60': fields.float(u'31/60',readonly=True),
        'days_due_61to90': fields.float(u'61/90',readonly=True),
        'days_due_91to120': fields.float(u'91/120',readonly=True),
        'days_due_121togr': fields.float(u'+121',readonly=True),
        'invoice_ref': fields.char('Their Invoice',size=25,readonly=True),
        'invoice_id': fields.many2one('account.invoice', 'Invoice', readonly=True),
        'comment': fields.text('Notes',readonly=True),
     }

    _order = 'date_due'

    def init(self, cr):
        """
        @author        Ursa Information Systems
        @description   Populate supplier aging view with up to date data on load
        @modified      2013-09-24
        """

        query="""                                                                                                             
                SELECT * from (            
                SELECT l.id as id, l.partner_id as partner_id, res_partner.name as "partner_name",
                    CASE WHEN ai.id is not null THEN ai.date_due ElSE l.date_maturity END as "date_due",
                    days_due as "avg_days_overdue", 
                    l.date as "oldest_invoice_date",
                    CASE WHEN (l.credit - l.debit) > 0 and ai.id is not null THEN ai.residual 
                         WHEN (l.credit - l.debit) < 0 and ai.id is not null THEN -1*ai.residual
                         ELSE l.credit - l.debit END as "total",
                    CASE WHEN (l.credit - l.debit) > 0 and (days_due BETWEEN 01 AND  30) and ai.id is not null then ai.residual
                         WHEN (l.credit - l.debit) < 0 and (days_due BETWEEN 01 AND  30) and ai.id is not null then -1*ai.residual 
                         WHEN (days_due BETWEEN 01 and 30) and ai.id is null THEN l.credit - l.debit ELSE 0 END  AS "days_due_01to30", 
                    CASE WHEN (l.credit - l.debit) > 0 and (days_due BETWEEN 31 AND  60) and ai.id is not null then ai.residual 
                         WHEN (l.credit - l.debit) < 0 and (days_due BETWEEN 31 AND  60) and ai.id is not null then -1*ai.residual 
                         WHEN (days_due BETWEEN 31 and 60) and ai.id is null THEN l.credit - l.debit ELSE 0 END  AS "days_due_31to60", 
                    CASE WHEN (l.credit - l.debit) > 0 and (days_due BETWEEN 61 AND  90) and ai.id is not null then ai.residual 
                         WHEN (l.credit - l.debit) < 0 and (days_due BETWEEN 61 AND  90) and ai.id is not null then -1*ai.residual 
                         WHEN (days_due BETWEEN 61 and 90) and ai.id is null THEN l.credit - l.debit ELSE 0 END  AS "days_due_61to90", 
                    CASE WHEN (l.credit - l.debit) > 0 and (days_due BETWEEN 91 AND 120) and ai.id is not null then ai.residual 
                         WHEN (l.credit - l.debit) < 0 and (days_due BETWEEN 91 AND 120) and ai.id is not null then -1*ai.residual 
                         WHEN (days_due BETWEEN 91 and 120) and ai.id is null THEN l.credit - l.debit ELSE 0 END  AS "days_due_91to120",
                    CASE WHEN (l.credit - l.debit) > 0 and days_due >= 121 and ai.id is not null then ai.residual 
                         WHEN (l.credit - l.debit) < 0 and days_due >= 121 and ai.id is not null then -1*ai.residual 
                         WHEN days_due >= 121 and ai.id is null THEN l.credit - l.debit ELSE 0 END AS "days_due_121togr",
                    CASE when (l.credit - l.debit) > 0 and days_due <= 0 and ai.id is not null then ai.residual 
                         WHEN (l.credit - l.debit) < 0 and days_due <= 0 and ai.id is not null then -1*ai.residual 
                         WHEN days_due <= 0 and ai.id is null THEN l.credit - l.debit ELSE 0 END as "current",
                    CASE when days_due < 0 THEN 0 ELSE days_due END as "max_days_overdue",
                    ai.supplier_invoice_number as "invoice_ref",
                    ai.id as "invoice_id", ai.comment
                   
                    FROM account_move_line as l     
                INNER JOIN         
                  (     
                   SELECT lt.id, 
                   CASE WHEN inv.date_due is null then 0
                   WHEN inv.id is not null THEN EXTRACT(DAY FROM (now() - inv.date_due)) 
                   ELSE EXTRACT(DAY FROM (now() - lt.date_maturity)) END AS days_due             
                   FROM account_move_line lt LEFT JOIN account_invoice inv on lt.move_id = inv.move_id   
                ) DaysDue       
                ON DaysDue.id = l.id               
                 
                INNER JOIN account_account       
                   ON account_account.id = l.account_id              
                INNER JOIN res_company              
                   ON account_account.company_id = res_company.id             
                INNER JOIN account_move                
                   ON account_move.id = l.move_id           
                LEFT JOIN account_invoice as ai    
                   ON ai.move_id = l.move_id           
                INNER JOIN res_partner        
                   ON res_partner.id = l.partner_id  
                WHERE account_account.active         
                  AND (account_account.type IN ('payable'))          
                  AND (l.reconcile_id IS NULL)  
                  AND account_move.state = 'posted'  
                  AND days_due IS NOT NULL
                ) sq
              """
            
        tools.drop_view_if_exists(cr, '%s'%(self._name.replace('.', '_')))
        cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s) 
        """%(self._name.replace('.', '_'), query) ) 
