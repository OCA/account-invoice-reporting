# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoice_pdf_proforma(self):
        res = super(
            AccountMove, self.with_context(hide_invoice_proforma=True)
        )._get_invoice_pdf_proforma()
        res["filename"] = self._get_invoice_report_filename() or res["filename"]
        return res
