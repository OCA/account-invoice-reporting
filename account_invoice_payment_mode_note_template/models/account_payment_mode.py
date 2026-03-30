# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from markupsafe import Markup

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountPaymentMode(models.Model):
    _inherit = "account.payment.mode"

    note = fields.Html(translate=True, sanitize_attributes=False, sanitize_tags=False)

    @api.constrains("note")
    def _check_note(self):
        invoice = self.env["account.move"].search([], limit=1)
        for rec in self:
            rec.render_note(invoice, raise_error=True)

    def render_note(self, invoice, raise_error=False):
        self.ensure_one()
        if not self.note:
            return ""
        try:
            note = self.with_context(lang=invoice.partner_id.lang).note
            result = self.env["mail.template"]._render_template(
                note, "account.move", [invoice.id], engine="qweb"
            )
            result = result.get(invoice.id, "")
            return Markup(result)
        except Exception as err:
            _logger.info(
                f"Failed to render note template for invoice {invoice.id!r}: {err}",
                exc_info=True,
            )
            if raise_error:
                raise UserError(_("Failed to render payment note template.")) from err
            return ""

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
