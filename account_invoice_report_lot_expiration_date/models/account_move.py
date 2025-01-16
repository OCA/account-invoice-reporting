# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import models
from odoo.tools.misc import format_date

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values(self):
        lot_values = super()._get_invoiced_lot_values()
        for lot_value in lot_values:
            lot = self.env["stock.lot"].browse(lot_value["lot_id"])
            lot_value["expiration_date"] = format_date(
                self.env,
                lot.expiration_date,
            )
        return lot_values
