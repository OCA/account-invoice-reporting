# -*- coding: utf-8 -*-
# Copyright 2014 Angel Moya <angel.moya@domatix.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_print(self):
        self.ensure_one()
        action_name = self.partner_id.invoice_report_id \
            and self.partner_id.invoice_report_id.report_name \
            or False
        if not action_name:
            return super(AccountInvoice, self).invoice_print()
        return self.env['report'].get_action(self, action_name)
