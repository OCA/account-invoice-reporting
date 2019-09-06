# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    show_in_report = fields.Boolean(default=True)

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        if self.price_unit > 0.0:
            self.show_in_report = True
        elif self.display_type:
            self.show_in_report = True
        else:
            self.show_in_report = False
            
class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    show_note_section = fields.Boolean("Show Notes and Sections", default=True, 
        help="When checked, notes and sections will be displayed on the printed invoice.")

    @api.onchange('show_note_section')
    def _onchange_show_special(self):
        for line in self.invoice_line_ids:
            if line.display_type:
                line.show_in_report = self.show_note_section
