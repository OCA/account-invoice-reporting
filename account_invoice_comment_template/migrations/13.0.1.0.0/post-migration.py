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
        SELECT ai.comment_template1_id, am.id
        FROM account_invoice ai
        JOIN account_move am ON ai.id = am.old_invoice_id
        WHERE ai.comment_template1_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO account_move_base_comment_template_rel
        (base_comment_template_id, account_move_id)
        SELECT ai.comment_template2_id, am.id
        FROM account_invoice ai
        JOIN account_move am ON ai.id = am.old_invoice_id
        WHERE ai.comment_template2_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
