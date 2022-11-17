# Copyright 2022 - Moduon
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    full_reconcile_payment_date = fields.Date(
        string="Payment Date",
        compute="_compute_full_reconcile_payment_date",
        store=True,
        compute_sudo=True,
        help="Date when the complete reconciliation of this invoice occurred.",
    )

    @api.depends("payment_state")
    def _compute_full_reconcile_payment_date(self):
        in_payment_states = {"paid", self._get_invoice_in_payment_state()}
        for move in self:
            if move.payment_state in in_payment_states:
                if not move.full_reconcile_payment_date:
                    payments = move._get_reconciled_payments().sorted(
                        "date", reverse=True
                    )
                    move.full_reconcile_payment_date = (
                        payments[:1].date or fields.Date.today()
                    )
                continue
            move.full_reconcile_payment_date = None
