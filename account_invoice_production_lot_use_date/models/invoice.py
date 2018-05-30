# -*- coding: utf-8 -*-
# Copyright 2018 Nicola Malcontenti <nicola.malcontenti@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def _compute_line_lots(self):
        res = super(AccountInvoice, self)._compute_line_lots()
        for line in self:
            if line.prod_lot_ids:
                note = u'<ul>'
                date = False
                for lot in line.prod_lot_ids:
                    if lot.use_date:
                        date =(
                            lot.use_date.split(" ")[0].split("-")[2] + "/" +
                            lot.use_date.split(" ")[0].split("-")[1] + "/" +
                            lot.use_date.split(" ")[0].split("-")[0]
                        )
                        note += u'<li>S/N' + unicode(
                            lot.name) + ' - ' + unicode(date) + '</li>'
                    else:
                        note += u'<li>S/N' + unicode(lot.name)'</li>'
                note += u'</ul>'
                line.lot_formatted_note = note
