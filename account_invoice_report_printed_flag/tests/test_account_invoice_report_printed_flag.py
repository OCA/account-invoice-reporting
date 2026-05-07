from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestReportPrintedFlagAccount(AccountTestInvoicingCommon):
    """
    Test suite for account_invoice_report_printed_flag.
    Covers:
    - printed flag behavior
    - log creation
    - printed report names computation
    - multi-record handling
    - non-configured reports
    - UI actions
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        # ---------------------------
        # ACCOUNT (provided by AccountTestInvoicingCommon)
        # ---------------------------
        cls.account = cls.company_data["default_account_receivable"]
        # ---------------------------
        # ACCOUNT MOVE (invoice)
        # ---------------------------
        cls.move = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.partner_a.id,
                "company_id": cls.company.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test line",
                            "quantity": 1,
                            "price_unit": 100,
                            "account_id": cls.account.id,
                        },
                    )
                ],
            }
        )
        # ---------------------------
        # QWEB TEMPLATE
        # ---------------------------
        cls.env["ir.ui.view"].create(
            {
                "name": "test_account_report_template",
                "type": "qweb",
                "key": "account_invoice_report_printed_flag.test_template",
                "arch": """
                <t t-name="account_invoice_report_printed_flag.test_template">
                    <t t-foreach="docs" t-as="o">
                        <div>
                            <span t-esc="o.id"/>
                        </div>
                    </t>
                </t>
            """,
            }
        )
        # ---------------------------
        # REPORT
        # ---------------------------
        cls.report = cls.env["ir.actions.report"].create(
            {
                "name": "Test Account Report",
                "model": "account.move",
                "report_type": "qweb-pdf",
                "report_name": "account_invoice_report_printed_flag.test_template",
            }
        )
        # ---------------------------
        # CONFIG
        # ---------------------------
        cls.config = cls.env["report.printed.config"].create(
            {
                "name": "Account Config",
                "model_id": cls.env["ir.model"]._get("account.move").id,
                "company_id": cls.company.id,
                "report_printed_log_active": True,
                "report_printed_names_active": True,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "report_id": cls.report.id,
                        },
                    )
                ],
            }
        )

    # ---------------------------
    # TESTS
    # ---------------------------
    def test_printed_flag(self):
        """Printing should mark move as printed"""
        self.assertFalse(self.move.printed)
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        self.move.invalidate_recordset()
        self.assertTrue(self.move.printed)

    def test_log_created(self):
        """Printing should create a log entry"""
        self.env["report.printed.log"].search([]).unlink()
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        logs = self.env["report.printed.log"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", self.move.id),
            ]
        )
        self.assertTrue(logs)

    def test_printed_report_names(self):
        """Printed report names should be computed"""
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        self.move.invalidate_recordset()
        self.assertTrue(self.move.printed_report_names)
        self.assertIn("Test Account Report", self.move.printed_report_names)

    def test_multiple_records(self):
        """Batch printing should mark all moves"""
        move2 = self.move.copy()
        self.report._render_qweb_pdf(
            self.report.report_name,
            (self.move | move2).ids,
        )
        self.move.invalidate_recordset()
        move2.invalidate_recordset()
        self.assertTrue(self.move.printed)
        self.assertTrue(move2.printed)

    def test_multiple_logs(self):
        """Multiple prints should create multiple logs"""
        self.env["report.printed.log"].search([]).unlink()
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        logs = self.env["report.printed.log"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", self.move.id),
            ]
        )
        self.assertEqual(
            len(logs),
            2,
            "Each report execution should create a separate log entry.",
        )

    def test_report_not_configured(self):
        """Non-configured report should not mark printed or create logs."""
        other_report = self.env["ir.actions.report"].create(
            {
                "name": "Other Report",
                "model": "account.move",
                "report_type": "qweb-pdf",
                "report_name": "account_invoice_report_printed_flag.test_template",
            }
        )
        self.env["report.printed.log"].search([]).unlink()
        self.move.write({"printed": False})
        other_report._render_qweb_pdf(
            other_report.report_name,
            self.move.ids,
        )
        self.move.invalidate_recordset()
        logs = self.env["report.printed.log"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", self.move.id),
            ]
        )
        self.assertFalse(self.move.printed)
        self.assertFalse(logs)

    def test_action_view_printed_logs(self):
        """UI action should return correct domain."""
        action = self.move.action_view_printed_logs()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "report.printed.log")
        self.assertEqual(action["view_mode"], "tree")
        self.assertIn(
            ("res_model", "=", "account.move"),
            action["domain"],
        )
        self.assertIn(
            ("res_id", "=", self.move.id),
            action["domain"],
        )

    def test_account_move_has_printed_mixin_fields(self):
        """Account moves should expose fields provided by the printed mixin."""
        self.assertIn("printed", self.move._fields)
        self.assertIn("printed_log_ids", self.move._fields)
        self.assertIn("printed_report_names", self.move._fields)

    def test_log_values(self):
        """Printed log should contain account move metadata."""
        self.env["report.printed.log"].search([]).unlink()
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        log = self.env["report.printed.log"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", self.move.id),
            ],
            limit=1,
        )
        self.assertTrue(log)
        self.assertEqual(log.res_model, "account.move")
        self.assertEqual(log.res_id, self.move.id)
        self.assertEqual(log.report_id, self.report)
        self.assertEqual(log.company_id, self.company)
        self.assertEqual(log.user_id, self.env.user)

    def test_logs_disabled(self):
        """Logs should not be created when disabled in configuration."""
        self.config.write(
            {
                "report_printed_log_active": False,
                "report_printed_names_active": False,
            }
        )
        self.env["report.printed.log"].search([]).unlink()
        self.report._render_qweb_pdf(
            self.report.report_name,
            self.move.ids,
        )
        logs = self.env["report.printed.log"].search(
            [
                ("res_model", "=", "account.move"),
                ("res_id", "=", self.move.id),
            ]
        )
        self.assertFalse(logs)
