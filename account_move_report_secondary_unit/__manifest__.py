# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Move Report Secondary Unit",
    "summary": """
        Show the secondary unit of measure and the secondary quantity in invoice reports
    """,
    "author": "Solvos, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "depends": ["sale_order_secondary_unit"],
    "data": ["report/report_invoice_document.xml"],
    "installable": True,
}
