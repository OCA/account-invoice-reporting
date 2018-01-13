# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


tables_renames = [
    (
        'base_condition_template',
        'base_comment_template'
    ),
]


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_tables(cr, tables_renames)
