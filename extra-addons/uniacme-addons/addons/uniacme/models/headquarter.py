# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import pytz


# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]
def _tz_get(self):
    return _tzs


class Headquarter(models.Model):
    _name = "uniacme.headquarter"
    _description = "Headquarter"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]

    name = fields.Char("Headquarter", required=True, tracking=True)
    country_id = fields.Many2one('res.country', string="Country", tracking=True)
    tz = fields.Selection(_tzs, string='Timezone', default=lambda self: self._context.get('tz'))
    active = fields.Boolean('Active', default=True, tracking=True)

    def uniacme_headquarter_view_form(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Headquarter"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": self._name,
            "res_id": self.id,
            "target": "current",
        }