# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class Career(models.Model):
    _name = "uniacme.career"
    _description = "Career"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]

    name = fields.Char("Career", required=True, tracking=True)
    active = fields.Boolean('Active', default=True, tracking=True)

    def uniacme_career_view_form(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Career"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": self._name,
            "res_id": self.id,
            "target": "current",
        }