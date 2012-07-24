# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
from report import report_sxw
import pooler

class account_invoice_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_invoice_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
            'company_vat': self._get_company_vat,
        })
    
    
    def _get_company_vat(self):
        res_users_obj=pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr, self.uid,self.uid).company_id.partner_id.vat
        if company_vat:
            return company_vat
        else:
            return False

report_sxw.report_sxw('report.account.invoice.webkit',
                       'account.invoice',
                       'addons/invoice_webkit/report/account_invoice.mako',
                       parser=account_invoice_report)
