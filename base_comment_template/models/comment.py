# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2020 NextERP Romania SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BaseCommentTemplate(models.Model):
    _name = "base.comment.template"
    _description = "Base comment template"

    active = fields.Boolean(default=True)

    name = fields.Char(string="Comment summary", required=True,)

    position = fields.Selection(
        selection=[("before_lines", "Before lines"), ("after_lines", "After lines")],
        required=True,
        default="before_lines",
        help="Position on document",
    )

    text = fields.Html(string="Comment", translate=True, required=True, sanitize=False)

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        help="If set, it'll only be available for this company",
        ondelete="cascade",
        index=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        ondelete="cascade",
        help="If set, the comment template will be available " "only for this partner.",
    )

    model_id = fields.Many2one(
        "ir.model",
        string="IR Model",
        ondelete="cascade",
        help="If set, the comment template will be available "
        "only for related model.",
    )

    model = fields.Char(related="model_id.model", index=True, store=True)

    domain = fields.Char(string="Domain", required=True, default="[]")
    # Only one default template per model_id and domain
    default = fields.Boolean(default=True)

    def write(self, vals):
        templates = self.env["base.comment.template"].search([])
        if vals.get("default"):
            for temp in self:
                # Replace previous default with the new one
                prev_default = templates.filtered(
                    lambda t: t.default
                    and t.model_id == temp.model_id
                    and t.domain == temp.domain
                    and t.position == temp.position
                    and t.id != temp.id
                )
                if prev_default:
                    prev_default.default = False
        result = super(BaseCommentTemplate, self).write(vals)
        # You cannot set default template on one assigned to a partner
        for temp in templates:
            if temp.partner_id and temp.default:
                temp.default = False
        return result
