
from ast import Str
from email.policy import default
from operator import index
import string
from tokenize import String
import pytz
from lxml import etree
from odoo import models, fields, api,  _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Patient record record'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    #_order = "appointment_date desc"
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.order') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    

    name = fields.Char(string = "Id de la cita", required = True, copy = False, readonly = True,
                            index = True, default = lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string = "Id del paciente", required = True)
    patient_full_name = fields.Char(string = "Nombre del paciente", related='patient_id.patien_full_name')
    patient_age = fields.Integer(string = "Edad", related='patient_id.patient_age')
    active = fields.Boolean(default = True, string = "Cita activa")
    notes = fields.Text(string = "Notas importantes")
    appointment_date = fields.Date(string = "Fecha", required = True)
    appointment_state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'confirmado'),
        ('done', 'Archivar'),
        ('cancel', 'Cancelado'),
    ], string="Estado", readonly=True,  default='draft')


    def action_confirm(self):
        self.write({'appointment_state':'confirm'})
            
    def action_done(self):
        self.write({'appointment_state':'done'})
        self.write({'active':'False'})
            
    def action_cancel(self):
        self.write({'appointment_state':'cancel'})

    def action_draft(self):
        self.write({'appointment_state':'draft'})


    





