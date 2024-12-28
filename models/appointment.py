# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'appointment Master'
    _rec_name = 'patient_id'
    _rec_names_search = ['reference', 'patient_id']

    reference = fields.Char(default="New")
    patient_id = fields.Many2one('hospital.patient', copy=False, ondelete='restrict')
    date_appointment = fields.Date('Date')
    note = fields.Text()
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), 
                   ('confirmed', 'Confirmed'),
                   ('ongoing', 'Ongoing'),
                   ('done', 'Done'),
                   ('cancel', 'Cancelled'),
                   ],
        default='draft', )
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', 'Lines')
    total_qty = fields.Float(compute='_compute_total_qty', store=True)
    date_of_birth = fields.Date(related='patient_id.date_of_birth', store=True)

    def action_draft(self):
        self.state = 'draft'
    def action_confirm(self):
        self.state = 'confirmed'
    def action_ongoing(self):
        self.state = 'ongoing'
    def action_done(self):
        self.state = 'done'
    def action_cancel(self):
        self.state = 'cancel'
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"
    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            # total_qty = 0
            # for line in rec.appointment_line_ids:
            #     total_qty += line.qty
            # rec.total_qty = total_qty
            rec.total_qty = sum(rec.appointment_line_ids.mapped('qty'))

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(values)

class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment')
    product_id = fields.Many2one('product.product')
    qty = fields.Float('Quantity')
    
