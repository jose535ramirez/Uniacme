# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request        
from odoo.exceptions import ValidationError
from pytz import timezone
from datetime import datetime

class UniAcmeVoting(http.Controller):
    @http.route('/vote', type='http', auth='public', website=True)
    def vote_login(self, **kw):
        return request.render('uniacme.vote_login_template', {})

    @http.route('/vote/selection', type='http', auth='public', website=True)
    def vote_selection(self, vat=None, **kw):
        student = request.env['res.partner'].sudo().search([('vat', '=', vat), ('partner_type', '=', 'student')], limit=1)
        if not student:
            return request.render('uniacme.vote_login_template', {'error': 'Student not found'})
        votes = request.env['voting.process'].sudo().search([('state', '=', 'open')])
        return request.render('uniacme.vote_selection_template', {'student': student, 'votes': votes})

    @http.route('/vote/candidate', type='http', auth='public', website=True)
    def vote_candidate(self, vat=None, vote_id=None, **kw):
        student = request.env['res.partner'].sudo().search([('vat', '=', vat), ('partner_type', '=', 'student')], limit=1)
        vote = request.env['voting.process'].sudo().browse(int(vote_id))
        candidates = vote.candidate_ids
        return request.render('uniacme.vote_candidate_template', {'student': student, 'vote': vote, 'candidates': candidates})

    @http.route('/vote/confirm', type='http', auth='public', website=True, methods=['POST'])
    def vote_confirm(self, vat=None, vote_id=None, candidate_id=None, **kw):
        student = request.env['res.partner'].sudo().search([('vat', '=', vat), ('partner_type', '=', 'student')], limit=1)
        vote = request.env['voting.process'].sudo().browse(int(vote_id))
        candidate = request.env['res.partner'].sudo().browse(int(candidate_id))

        if vote.state != 'open':
            return request.render('uniacme.vote_confirm_template', {
                'student': student,
                'vote': vote,
                'candidate': candidate,
                'message': 'You can only vote when the process is open.'
            })
        
        if not vote.tz:
            return request.render('uniacme.vote_confirm_template', {
                'student': student,
                'vote': vote,
                'candidate': candidate,
                'message': 'Voting process does not have a timezone configured.'
            })

        tz = timezone(vote.tz)
        now = datetime.now(tz)
        date_start = vote.date_start.astimezone(tz)
        end_date = vote.date.astimezone(tz)
        if not (date_start <= now <= end_date):
            return request.render('uniacme.vote_confirm_template', {
                'student': student,
                'vote': vote,
                'candidate': candidate,
                'message': 'Voting is not allowed at this date/time.'
            })

        already_voted = request.env['voting.line'].sudo().search_count([
            ('student_id', '=', student.id),
            ('process_id', '=', vote.id)
        ])
        if already_voted:
            return request.render('uniacme.vote_confirm_template', {
                'student': student,
                'vote': vote,
                'candidate': candidate,
                'message': 'You have already voted in this process.'
            })

        request.env['voting.line'].sudo().create({
            'student_id': student.id,
            'process_id': vote.id,
            'candidate_id': candidate.id,
        })

        return request.render('uniacme.vote_confirm_template', {
            'student': student,
            'vote': vote,
            'candidate': candidate,
            'message': 'Vote successfully registered!'
        })
