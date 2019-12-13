# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPaymentModeNoteTemplate(models.TransientModel):
    _name = "account.payment.mode.note.template"
    _description = "Payment Mode Note Template"

    payment_mode_id = fields.Many2one(
        comodel_name="account.payment.mode",
        string="",
        required=True,
        ondelete="cascade",
    )
    note = fields.Html(string="Note", translate=True)
    model_object_field = fields.Many2one(
        "ir.model.fields",
        string="Field",
        help="Select target field from the related document model.\n"
        "If it is a relationship field you will be able to select "
        "a target field at the destination of the relationship.",
    )
    sub_object = fields.Many2one(
        "ir.model",
        "Sub-model",
        readonly=True,
        help="When a relationship field is selected as first field, "
        "this field shows the document model the relationship goes to.",
    )
    sub_model_object_field = fields.Many2one(
        "ir.model.fields",
        "Sub-field",
        help="When a relationship field is selected as first field, "
        "this field lets you select the target field within the "
        "destination document model (sub-model).",
    )
    null_value = fields.Char(
        "Default Value",
        help="Optional value to use if the target field is " "empty",
    )
    copyvalue = fields.Char(
        "Placeholder Expression",
        help="Final placeholder expression, "
        "to be copy-pasted in the desired template field.",
    )

    def build_expression(self, field_name, sub_field_name, null_value):
        return self.env["mail.template"].build_expression(
            field_name, sub_field_name, null_value
        )

    @api.onchange("model_object_field", "sub_model_object_field", "null_value")
    def onchange_sub_model_object_value_field(self):
        if self.model_object_field:
            if self.model_object_field.ttype in [
                "many2one",
                "one2many",
                "many2many",
            ]:
                model = self.env["ir.model"]._get(
                    self.model_object_field.relation
                )
                if model:
                    self.sub_object = model.id
                    self.copyvalue = self.build_expression(
                        self.model_object_field.name,
                        self.sub_model_object_field
                        and self.sub_model_object_field.name
                        or False,
                        self.null_value or False,
                    )
            else:
                self.sub_object = False
                self.sub_model_object_field = False
                self.copyvalue = self.build_expression(
                    self.model_object_field.name,
                    False,
                    self.null_value or False,
                )
        else:
            self.sub_object = False
            self.copyvalue = False
            self.sub_model_object_field = False
            self.null_value = False

    @api.multi
    def validate(self):
        self.ensure_one()
        self.payment_mode_id.note = self.note
        return True
