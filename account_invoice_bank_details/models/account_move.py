# Copyright 2020-2021 Camptocamp - Vincent Renaville
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("currency_id", "company_id.partner_id")
    def _compute_partner_bank_id(self):
        for record in self:
            if record.currency_id:
                # try to find bank account by currency
                partner_bank = self.env["res.partner.bank"].search(
                    [
                        ("currency_id", "=", self.currency_id.id),
                        ("partner_id", "=", self.company_id.partner_id.id),
                    ],
                    limit=1,
                )

                # if not found take first bank account of the company
                if not partner_bank:
                    partner_bank = self.env["res.partner.bank"].search(
                        [("partner_id", "=", self.company_id.partner_id.id)], limit=1
                    )

                record.partner_bank_id = partner_bank.id

            else:
                return super()._compute_partner_bank_id
