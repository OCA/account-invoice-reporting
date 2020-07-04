# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_obj = self.env["ir.model"].search([("model", "=", "res.partner")])
        self.partner_id = self.env.ref("base.res_partner_12")
        self.partner2_id = self.env.ref("base.res_partner_10")
        self.company = self.env["res.company"].create({"name": "company_1"})
        self.before_template_id = self.env["base.comment.template"].create(
            {
                "name": "Comment before lines",
                "position": "before_lines",
                "text": "Text before lines",
                "model_id": self.partner_obj.id,
                "default": True,
            }
        )
        self.after_template_id = self.env["base.comment.template"].create(
            {
                "name": "Comment after lines",
                "position": "after_lines",
                "text": "Text after lines",
                "model_id": self.partner_obj.id,
                "default": True,
            }
        )

    def test_general_template(self):
        # Check getting default comment template
        templ = self.partner_id.get_comment_template("before_lines")
        self.assertEqual(templ, "Text before lines")
        templ = self.partner_id.get_comment_template("after_lines")
        self.assertEqual(templ, "Text after lines")
        # If no default is set, return False
        self.before_template_id.default = False
        templ = self.partner_id.get_comment_template("before_lines")
        self.assertFalse(templ)

    def test_company_general_template(self):
        # Check getting default comment template company
        self.before_template_id.company_id = self.company
        templ = self.partner_id.get_comment_template("before_lines")
        self.assertFalse(templ)
        templ = self.partner_id.get_comment_template(
            "before_lines", company_id=self.company.id
        )
        self.assertEqual(templ, "Text before lines")
        templ = self.partner_id.get_comment_template("after_lines")
        self.assertEqual(templ, "Text after lines")
        # If no default is set, return False
        self.before_template_id.default = False
        templ = self.partner_id.get_comment_template("before_lines")
        self.assertFalse(templ)

    def test_partner_template(self):
        # Check getting the comment template if partner is set
        self.before_template_id.partner_id = self.partner2_id
        templ = self.partner_id.get_comment_template(
            "before_lines", partner_id=self.partner2_id.id
        )
        self.assertEqual(templ, "Text before lines")
        templ = self.partner_id.get_comment_template(
            "before_lines", partner_id=self.partner_id.id
        )
        self.assertFalse(templ)
        templ = self.partner_id.get_comment_template("after_lines")
        self.assertEqual(templ, "Text after lines")

    def test_partner_template_domain(self):
        # Check getting the comment template if domain is set
        self.before_template_id.partner_id = self.partner2_id
        self.before_template_id.domain = "[('id', 'in', %s)]" % self.partner_id.ids
        templ = self.partner_id.get_comment_template(
            "before_lines", partner_id=self.partner2_id.id
        )
        self.assertEqual(templ, "Text before lines")
        templ = self.partner2_id.get_comment_template(
            "before_lines", partner_id=self.partner2_id.id
        )
        self.assertFalse(templ)

    def test_company_partner_template_domain(self):
        # Check getting the comment template with company and if domain is set
        self.before_template_id.company_id = self.company
        templ = self.partner_id.get_comment_template("before_lines")
        self.assertFalse(templ)
        templ = self.partner_id.get_comment_template(
            "before_lines", company_id=self.company.id
        )
        self.assertEqual(templ, "Text before lines")
        self.before_template_id.partner_id = self.partner2_id
        self.before_template_id.domain = "[('id', 'in', %s)]" % self.partner_id.ids
        templ = self.partner_id.get_comment_template(
            "before_lines", partner_id=self.partner2_id.id
        )
        self.assertFalse(templ)
        self.before_template_id.company_id = self.env.user.company_id
        templ = self.partner_id.get_comment_template(
            "before_lines", partner_id=self.partner2_id.id
        )
        self.assertEqual(templ, "Text before lines")
        templ = self.partner2_id.get_comment_template(
            "before_lines", partner_id=self.partner2_id.id
        )
        self.assertFalse(templ)

    def test_default_template_write(self):
        # Check setting default template will change previous record default
        new_template = self.env["base.comment.template"].create(
            {
                "name": "Comment before lines",
                "position": "before_lines",
                "text": "Text before lines",
                "model_id": self.partner_obj.id,
                "default": False,
            }
        )
        new_template.default = True
        self.assertFalse(self.before_template_id.default)
