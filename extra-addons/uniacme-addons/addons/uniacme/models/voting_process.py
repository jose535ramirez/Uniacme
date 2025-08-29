from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
import pytz


# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]
def _tz_get(self):
    return _tzs


class VotingProcess(models.Model):
    
    _name = "voting.process"
    _description = "Voting Process"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]
    _rec_name = "description"

    description = fields.Text("Description", required=True, tracking=True)
    date_start = fields.Datetime("Start Date", required=True, tracking=True)
    date = fields.Datetime("End Date", required=True, tracking=True)
    country_id = fields.Many2one('res.country', string="Country", tracking=True)
    tz = fields.Selection(_tzs, string='Timezone', default=lambda self: self._context.get('tz'))
    candidate_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Candidates",
        domain=[('partner_type', '=', 'candidate')],
        required=True,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string="State", default='draft', tracking=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    candidate_vote_info = fields.Json(string="Candidate Vote Info", compute="_compute_candidate_vote_info", default=list)

    def _compute_candidate_vote_info(self):
        for rec in self:
            info = []
            if rec.candidate_ids:
                for candidate in rec.candidate_ids:
                    vote_count = rec.env['voting.line'].search_count([
                        ('process_id', '=', rec.id),
                        ('candidate_id', '=', candidate.id)
                    ])
                    info.append([candidate.id, candidate.name, vote_count])
            rec.candidate_vote_info = info

    def start_voting(self):
        for rec in self:
            missing = []
            if not rec.description:
                missing.append('description')
            if not rec.date_start:
                missing.append('date_start')
            if not rec.date:
                missing.append('date')
            if not rec.tz:
                missing.append('tz')
            if not rec.candidate_ids:
                missing.append('candidate_ids')
            if missing:
                raise ValidationError(_('The process cannot be started. The following required fields are missing: %s') % ', '.join(missing))
            rec.state = 'open'


class VotingLine(models.Model):
    _name = "voting.line"
    _description = "Voting Line"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]

    process_id = fields.Many2one("voting.process", string="Voting Process", required=True)
    candidate_id = fields.Many2one("res.partner", string="Candidate", required=True)
    student_id = fields.Many2one("res.partner", string="Student", required=True)
    active = fields.Boolean("Active", default=True)