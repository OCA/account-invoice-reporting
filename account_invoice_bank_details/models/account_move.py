# Copyright 2020-2021 Camptocamp - Vincent Renaville
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        # try to find bank account by currency
        bank = self.env['res.partner.bank'].search([
            ('currency_id', '=', self.currency_id.id),
            ('partner_id', '=', self.company_id.partner_id.id),
            ], limit=1)
        # if not found take first bank account of the company
        if not bank:
            bank = self.env['res.partner.bank'].search(
                [('partner_id', '=', self.company_id.partner_id.id)],
                limit=1
            )
        
        self.invoice_partner_bank_id = bank.id


