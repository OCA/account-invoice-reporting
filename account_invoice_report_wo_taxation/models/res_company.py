# Copyright 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    account_move_hidden_report_tax = fields.Boolean(
        string="Hide Taxes on Invoices Report",
        default=True,
        help="If enabled, taxes will not be shown on the invoice report.",
    )
