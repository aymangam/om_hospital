# -*- coding: utf-8 -*-

from odoo import models, fields

class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _order = 'sequence,id'

    name = fields.Char(string='Name', required=1)
    sequence = fields.Integer(default=10)



