# Copyright 2020 NextERP Romania SRL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import safe_eval


class Base(models.AbstractModel):
    _inherit = "base"

    def get_comment_template(self, position=False, company_id=False, partner_id=False):
        self.ensure_one()
        template = False
        if not company_id:
            company_id = self.env.user.company_id.id
        default_dom = [
            ("model", "=", self._name),
            ("position", "=", position),
            ("default", "=", True),
            "|",
            ("company_id", "=", company_id),
            ("company_id", "=", False),
        ]
        templates = self.env["base.comment.template"].search(default_dom)
        if partner_id:
            partner_dom = [
                ("model", "=", self._name),
                ("position", "=", position),
                ("partner_id", "=", partner_id),
                "|",
                ("company_id", "=", company_id),
                ("company_id", "=", False),
            ]
            part_templates = self.env["base.comment.template"].search(partner_dom)
            lang = self.env["res.partner"].browse(partner_id).lang
            if part_templates:
                templates = part_templates.with_context({"lang": lang})
        if templates:
            for templ in templates:
                if self in self.search(safe_eval(templ.domain or "[]")):
                    template = templ
                    break
        if not template:
            return False
        return self.env["mail.template"]._render_template(
            template.text, self._name, self.id, post_process=True
        )
