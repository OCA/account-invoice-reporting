# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    multi_due = fields.Boolean(string="Multiple date due", compute="_compute_multi_due")
    multi_date_due = fields.Char(string="Due Dates", compute="_compute_multi_date_due")

    @api.depends("invoice_payment_term_id")
    def _compute_multi_due(self):
        for record in self:
            record.multi_due = len(record.invoice_payment_term_id.line_ids) > 1

    def _compute_multi_date_due(self):
        lang = self.env.context.get("lang") or "en_US"
        date_format = self.env["res.lang"]._lang_get(lang).date_format
        for record in self:
            record.multi_date_due = " ".join(
                fields.Date.from_string(due[0]).strftime(date_format)
                for due in record.get_multi_due_list()
            )

    def get_multi_due_list(self):
        self.ensure_one()
        due_list = []
        if self.type in ["in_invoice", "in_refund"]:
            due_move_line_ids = self.line_ids.filtered(
                lambda ml: ml.account_id.internal_type == "payable" and ml.date_maturity
            )
        else:
            due_move_line_ids = self.line_ids.filtered(
                lambda ml: ml.account_id.internal_type == "receivable"
                and ml.date_maturity
            )
        if self.currency_id != self.company_id.currency_id:
            due_list = [
                (ml.date_maturity, ml.amount_currency) for ml in due_move_line_ids
            ]
        else:
            due_list = [(ml.date_maturity, ml.balance) for ml in due_move_line_ids]
        due_list.sort()
        return due_list
