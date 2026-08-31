# Copyright 2022 Tecnativa - Carlos Roca
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    volume = fields.Float(digits="Volume")

    def _select(self) -> SQL:
        return SQL(
            """
                %s,
                COALESCE(
                    (product.volume *
                    (CASE WHEN move.move_type IN
                    ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END)
                    * line.quantity / uom_line.factor * uom_template.factor),
                    0.0
                ) as volume
            """,
            super()._select(),
        )
