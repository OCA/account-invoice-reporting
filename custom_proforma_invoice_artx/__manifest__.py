{
    "name": "Sale Proforma Custom Amount",
    "summary": (
        "Generate proforma invoices with custom down payment amount " "in Sale Orders."
    ),
    "version": "17.0.1.0.0",
    "category": "Sales",
    "author": "Areterix Technologies, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "license": "LGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "views/sale_order_views.xml",
        "report/report_proforma_invoice_template.xml",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "development_status": "Beta",
    "maintainers": ["umaniar-plus"],
}
