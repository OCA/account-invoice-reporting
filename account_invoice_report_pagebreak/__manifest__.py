# Copyright 2023 CGI37 (https://www.cgi37.com).
# @author Pierre Verkest <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Invoice report page break",
    "summary": "Control Page Breaks in PDF invoice report",
    "version": "14.0.1.0.0",
    "author": "Pierre Verkest, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "license": "AGPL-3",
    "category": "Accounting",
    "depends": [
        "account",
        "report_qweb_table_pagebreak",
    ],
    "data": [
        "reports/report_invoice.xml",
    ],
    "maintainers": ["petrus-v"],
}
