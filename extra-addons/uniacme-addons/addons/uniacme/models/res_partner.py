from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Contact(models.Model):
    _inherit = "res.partner"

    headquarter_id = fields.Many2one(
        comodel_name="uniacme.headquarter",
        string="Headquarter",
        tracking=True,
    )

    university_career_id = fields.Many2one(
        comodel_name="uniacme.career",
        string="University Career",
        tracking=True,
    )

    partner_type = fields.Selection([
        ('student', 'Student'),
        ('candidate', 'Candidate')
    ], string="Contact Type", required=True, tracking=True)

    @api.onchange('partner_type')
    def _onchange_partner_type(self):
        for partner in self:
            if partner.partner_type == 'candidate':
                partner.headquarter_id = False
                partner.university_career_id = False

    @api.constrains('vat')
    def _check_vat_unique(self):
        for partner in self:
            if partner.vat:
                existing = self.search([
                    ('vat', '=', partner.vat),
                    ('id', '!=', partner.id)
                ], limit=1)
                if existing:
                    raise ValidationError("You cannot create a contact with the same VAT.")
