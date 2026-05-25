# Copyright 2026 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_packaging_info(self):
        self.ensure_one()
        pkg_amnts = {}
        for move in self.move_line_ids.filtered("product_packaging_id"):
            pkg_amnts.setdefault(move.product_packaging_id, 0.0)
            pkg_amnts[move.product_packaging_id] += move.product_packaging_quantity
        if not pkg_amnts:
            return ""
        return ", ".join(f"{pq} {p.name}" for p, pq in pkg_amnts.items())
