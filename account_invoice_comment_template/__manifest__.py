# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Qubiq - Xavier Jiménez
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Invoice Comments Template",
    "summary": "Comments templates on invoice documents",
    "version": "13.0.1.1.1",
    "category": "Accounting & Finance",
    "author": "Camptocamp, Tecnativa, Odoo Community Association (OCA)",
    "development_status": "Mature",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account", "base_comment_template"],
    "data": [
        "views/account_move_view.xml",
        "views/base_comment_template_view.xml",
        "security/ir.model.access.csv",
        "views/report_invoice.xml",
    ],
}
