# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Account Invoice Line Sale Line Position",
    "summary": "Adds the related sale line position on invoice line.",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "depends": ["sale_order_line_position"],
    "data": ["views/account_move_views.xml", "report/invoice_report.xml"],
    "installable": True,
}
