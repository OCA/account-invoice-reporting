# Copyright 2026 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _get_rendering_context(self, report, docids, data):
        data = super()._get_rendering_context(report, docids, data)
        # Download and portal paths, the Send wizard fallback keeps the proforma
        if self.env.context.get("hide_invoice_proforma") or self.env.context.get(
            "proforma_invoice"
        ):
            data["proforma"] = False
        return data
