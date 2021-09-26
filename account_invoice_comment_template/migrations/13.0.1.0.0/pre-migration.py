# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # We need to create the table in order to prevent the computation. It will be
    # correctly generated later.
    openupgrade.logged_query(
        env.cr,
        """
        CREATE TABLE "account_move_base_comment_template_rel" ("temp" INTEGER )
        """,
    )
