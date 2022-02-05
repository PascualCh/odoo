
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
    patient_id = fields.Many2one('hospital.patient', string = "Nombre del paciente", required = True)
    patient_age = fields.Integer(string = "Edad", related='patient_id.patient_age')
    notes = fields.Text(string = "Notas importantes")
    appointment_date = fields.Date(String = "Fecha", required = True)




    





