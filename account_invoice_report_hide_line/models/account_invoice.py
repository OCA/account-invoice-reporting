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
        else:
            self.show_in_report = False
