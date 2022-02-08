import base64
from email.policy import default

from odoo import models, fields, modules, api, _
from odoo.exceptions import ValidationError


def get_default_img(name_image):
        with open(modules.get_module_resource('mod_exchanger', 'static/description', name_image),
              'rb') as f:
            return base64.b64encode(f.read())

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient record'
    _rec_name = 'patient_name'

    #agregar campos flotantes, enteros, tipo seleccion, boleanos
    #agregar en los parametros de creacion default,readonly,required, help
    
    # Informacion general
    patient_name = fields.Char(default = "Pedro", string = "Nombre paciente", help = "Nombre del paciente", required = True)
    patient_last_name = fields.Char(default = "Chavez", string = "Apellido del paciente", help = "Apellido del paciente", required = True)
    patien_full_name = fields.Char(string = 'Nombre completo' , compute = 'define_full_name')

    patient_state = fields.Boolean(default = True, string = "Vivo ", help = "Estado del paciente", required = True)
    patient_height = fields.Float(default = 1.75, string = "Estatura", help = "Estatura del paciente", required = False)
    patient_id = fields.Char(string='Matricula del paciente', required = True, copy = False, readonly = True,
                            index = True, default = lambda self: _('New'))
    patient_gender = fields.Selection([('male','Hombre'),('female','Mujer')], string = 'Genero del paciente' , default = 'male')
    patient_age_group = fields.Selection([('child','Menor'),('adult','Adulto'), ('older','Mayor')], string = 'Ciclo de vida' , compute = 'define_age_group')
    patient_grade = fields.Selection([('a','sin seguro'),('b','con seguro'),('c','Premium')], string = 'Tipo de paciente' , default = 'a')
    patient_age = fields.Integer(default = "20", string = "Edad del paciente", help = "Escriba la edad del paciente")
    patient_photo = fields.Image(default = get_default_img('id_default.png'), string = "Fotografia del paciente")
    patient_last_modify = fields.Datetime(default = fields.Datetime.now(), string = "Fecha de la ultima modificación")
    patient_appointment_count = fields.Integer(string="citas", compute = 'get_appointment_count')
    
    # Ultimas citas
    patient_appointment_data = fields.Many2one('hospital.appointment')
    patient_id_appointment = fields.Char(string = "Id de cita", related='patient_appointment_data.name')
    patient_date_appointment = fields.Date(string = "Fecha", related='patient_appointment_data.appointment_date')

    # Informacion de contacto
    patient_phone = fields.Char(default = "443-456-7895", string = "Numero telefonico", help = "Escriba el numero del paciente")
    patien_email = fields.Char(default = "pascual.ch@tekniu.mx", string = "Correo del paciente", help = "Escriba el correo electronico del paciente")

    # informacion de pago
    patient_payment_mode = fields.Selection([('a','Efectivo'),('b','tarjeta de debito'),('c','Tarjeta de credito')], string = 'Metodo de pago' , default = 'a')

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id','=', self.id)])
        self.patient_appointment_count = count

    
    def open_patient_appointments(self):
        return {
            'name':_('Citas'),
            'domain':[('patient_id','=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    def create_appointment(self):
        return {
            'name':_('Crear cita'),
            'domain':[],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_mode': 'form,tree',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    @api.onchange('patient_state','patient_photo')
    def onchange_modify(self):
        today = fields.Date.today()
        for rec in self:
            if self.patient_last_modify != today:
                self.patient_last_modify = fields.Datetime.now()

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age < 5:
                raise ValidationError(_("No podemos admitir menores de 2 años"))

    @api.depends('patient_name')
    def define_full_name(self):
        for rec in self:
            if(rec.patient_name):
                rec.patien_full_name = rec.patient_name + " " + rec.patient_last_name

    @api.depends('patient_age')
    def define_age_group(self):
        for rec in self:
            if(rec.patient_age):
                if(rec.patient_age < 18):
                    rec.patient_age_group = 'child'
                elif(rec.patient_age > 58):
                    rec.patient_age_group = 'older'
                else:
                    rec.patient_age_group = 'adult'


    @api.model
    def create(self, vals):
        if vals.get('patient_id', _('New')) == _('New'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('hospital.patient.order') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    