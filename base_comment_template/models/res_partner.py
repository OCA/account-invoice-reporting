# Copyright 2020 NextERP Romania SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    comment_template_ids = fields.One2many(
        "base.comment.template",
        "partner_id",
        string="Comment templates",
        company_dependent=True,
    )
