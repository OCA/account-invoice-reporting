# -*- coding: utf-8 -*-
# Copyright 2018 Nicola Malcontenti <nicola.malcontenti@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def _compute_line_lots(self):
        res = super(AccountInvoice, self)._compute_line_lots()
        lang = self.env['res.lang']._lang_get(self.env.lang)
        date_format = lang.date_format
        for line in self:
            if line.prod_lot_ids:
                note = u'<ul>'
                date = ""
                for lot in line.prod_lot_ids:
                    if lot.use_date:
                        date = datetime.strptime(
                            lot.use_date,
                            DEFAULT_SERVER_DATETIME_FORMAT).strftime(
                            date_format)
                        note += u'<li>S/N' + unicode(
                            lot.name) + ' - ' + unicode(date) + '</li>'
                    else:
                        note += u'<li>S/N ' + unicode(lot.name) + '</li>'
                note += u'</ul>'
                line.lot_formatted_note = note
