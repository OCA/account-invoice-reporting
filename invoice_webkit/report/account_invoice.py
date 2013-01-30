# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier, Vincent Renaville, Nicolas Bessi
#
#   @author Bessi Nicolas, Vincent Renaville
#
#
##############################################################################
import time

from openerp.report import report_sxw
from openerp import pooler

class AccountInvoice_Report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(AccountInvoice_Report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
            'company_vat': self._get_company_vat,
        })


    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr, self.uid, self.uid).company_id.partner_id.vat
        if company_vat:
            return company_vat
        else:
            return False

report_sxw.report_sxw('report.account.invoice.webkit',
                       'account.invoice',
                       'invoice_webkit/report/account_invoice.mako',
                       parser=AccountInvoice_Report)
