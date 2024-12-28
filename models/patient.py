# -*- coding: utf-8 -*-
from pickle import FALSE

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string='Name', required=1, tracking=1)
    date_of_birth = fields.Date(string='DOB', required=False)
    gander = fields.Selection([('male', 'Male'), ('female', 'Female'), ], required=False, )
    tag_ids = fields.Many2many('patient.tag', 'patient_tag_rel',
                               'patient_id', "tag_id", 'Tags')
    is_minor = fields.Boolean()
    guardian = fields.Char()

    @api.ondelete(at_uninstall=False)
    def _check_patient_appointments(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointment = rec.env['hospital.appointment'].search(domain)
            if appointment:
                raise ValidationError('You cannot delete the patient now. '
                                        '\nAppointment existing for this patient')

    @api.onchange('date_of_birth')
    def check_is_minor(self):
        today = fields.Datetime.today()
        for rec in self:
            if rec.date_of_birth:
                age = relativedelta(today, rec.date_of_birth).years
                age1 = today.year - rec.date_of_birth.year
                print(f"Age: {age} years")
                print(f"Age1: {age1} years")
                if age < 16:
                    rec.is_minor = True


