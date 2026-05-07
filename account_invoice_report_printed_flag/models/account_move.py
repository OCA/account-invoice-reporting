from odoo import models


class AccountMove(models.Model):
    """
    Extension of ``account.move`` to integrate with the
    ``report_printed_flag`` infrastructure via the mixin.

    This module adds:
    - A ``printed`` Boolean field (from mixin)
    - A ``printed_log_ids`` One2many relation to print logs (from mixin)
    - A ``printed_report_names`` computed Char field (from mixin)
    - An ``action_view_printed_logs()`` method (from mixin)

    All functionality is provided by ``report.printed.mixin``.
    """

    _name = "account.move"
    _inherit = ["account.move", "report.printed.mixin"]
