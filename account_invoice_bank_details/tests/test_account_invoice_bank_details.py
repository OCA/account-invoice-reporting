from odoo.addons.base.tests.common import BaseCommon


class TestAccountMove(BaseCommon):
    @classmethod
    def setUpClass(cls):
        """Configure and Created required data"""
        super().setUpClass()

        cls.currency_usd = cls.env.ref("base.USD")
        cls.company = cls.env.ref("base.main_company")
        cls.company.currency_id = cls.currency_usd.id
        cls.company_partner = cls.company.partner_id

        # Create a customer
        cls.customer = cls.env["res.partner"].create({"name": "Test Customer"})

        # Configure bank accounts for the company
        cls.bank_account_general = cls.env.ref("account.1_demo_bank_1")
        cls.bank_account_usd = cls.env["res.partner.bank"].create(
            {
                "acc_number": "USD001",
                "currency_id": cls.currency_usd.id,
                "partner_id": cls.company_partner.id,
            }
        )

        # Create an account moves
        cls.account_move = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "currency_id": cls.currency_usd.id,
                "partner_id": cls.customer.id,
                "company_id": cls.company.id,
            }
        )

    def test_partner_bank_id_with_currency(self):
        """Test that the partner_bank_id is correctly set based on currency."""
        self.assertEqual(
            self.account_move.partner_bank_id.id,
            self.bank_account_usd.id,
            "The partner bank should be set to the account matching the currency.",
        )

    def test_partner_bank_id_without_currency(self):
        """Test that the partner_bank_id falls back to the first available account."""
        self.bank_account_usd.currency_id = None
        self.account_move._compute_partner_bank_id()
        self.assertEqual(
            self.account_move.partner_bank_id.id,
            self.bank_account_general.id,
            "The partner bank should fall back to the first available account.",
        )
