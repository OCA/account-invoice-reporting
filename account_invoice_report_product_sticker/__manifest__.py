# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Account Invoice Report - Product Sticker",
    "summary": "Display Product Stickers on Invoice Reports",
    "version": "16.0.1.0.4",
    "development_status": "Alpha",
    "category": "Accounting/Accounting",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["Shide", "rafaelbn"],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "account",
        "product_sticker",
    ],
    "data": [
        "views/res_config_settings_view.xml",
        "views/account_move_view.xml",
        "views/report_invoice.xml",
    ],
}
