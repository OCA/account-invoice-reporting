# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO account_move_base_comment_template_rel
        (base_comment_template_id, account_move_id)
        SELECT bct.id AS base_comment_template_id, am.id AS account_move_id
        FROM account_move am
        JOIN base_comment_template bct ON bct.id = am.old_comment_template1_id
        WHERE am.old_comment_template1_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO account_move_base_comment_template_rel
        (base_comment_template_id, account_move_id)
        SELECT bct.id AS base_comment_template_id, am.id AS account_move_id
        FROM account_move am
        JOIN base_comment_template bct ON bct.id = am.old_comment_template2_id
        WHERE am.old_comment_template2_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
