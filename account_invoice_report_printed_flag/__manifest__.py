{
    "name": "Account Invoice Report Printed Flag",
    "summary": "Adds printed flag support to account moves",
    "version": "17.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "Binhex Systems Solutions S.L, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "depends": [
        "account",
        "report_printed_flag",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
    "development_status": "Alpha",
    "images": ["static/description/icon.png"],
}
