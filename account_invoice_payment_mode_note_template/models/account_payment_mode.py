# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, tools

from odoo.exceptions import UserError
from odoo.addons.mail.models.mail_template import (
    mako_safe_template_env,
    mako_template_env,
)

_logger = logging.getLogger(__name__)


class AccountPaymentMode(models.Model):

    _inherit = "account.payment.mode"

    note = fields.Html(string="Note", translate=True)

    @api.constrains('note')
    def _check_note(self):
        invoice = self.env['account.invoice'].search([], limit=1)
        for rec in self:
            rec.render_note(invoice, raise_error=True)

    @api.multi
    def render_note(self, invoice, raise_error=False):
        self.ensure_one()
        variables = {"object": invoice}
        if not self.note:
            return ""
        try:
            mako_env = (
                mako_safe_template_env
                if self.env.context.get("safe")
                else mako_template_env
            )
            template = mako_env.from_string(tools.ustr(self.note))
        except Exception:
            _logger.info(
                "Failed to load template %r", self.note, exc_info=True
            )
            if raise_error:
                raise UserError("Failed to load template %r", self.note)
        try:
            return template.render(variables)
        except Exception:
            _logger.info(
                "Failed to render template {!r} using values {!r}".format(
                    template, variables
                ),
                exc_info=True,
            )
            if raise_error:
                raise UserError(
                    "Failed to render template {!r} using values {!r}".format(
                        template, variables
                    )
                )
        return ""

    @api.multi
    def action_update_template_note(self):
        self.ensure_one()
        context = {
            "default_payment_mode_id": self.id,
            "default_note": self.note,
        }
        context.update(self.env.context)
        return {
            "type": "ir.actions.act_window",
            "name": "Update Payment Note Template",
            "res_model": "account.payment.mode.note.template",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "context": context,
        }
