import base64
from odoo import models, fields, modules, api, _

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
    patient_state = fields.Boolean(default = False, string = "Vivo ", help = "Estado del paciente", required = True)
    patient_height = fields.Float(default = 1.75, string = "Estatura", help = "Estatura del paciente", required = False)
    patient_id = fields.Char(string='Matricula del paciente', required = True, copy = False, readonly = True,
                            index = True, default = lambda self: _('New'))
    patient_gender = fields.Selection([('a','Hombre'),('b','Mujer')], string = 'Genero del paciente' , default = 'a')
    patient_grade = fields.Selection([('a','sin seguro'),('b','con seguro'),('c','Premium')], string = 'Tipo de paciente' , default = 'a')
    patient_photo = fields.Image(default = get_default_img('id_default.png'), string = "Fotografia del paciente")

    # Ultimos trtamientos


    # Informacion de contacto
    patient_phone = fields.Char(default = "443-456-7895", string = "Numero telefonico", help = "Escriba el numero del paciente")
    patien_email = fields.Char(default = "pascual.ch@tekniu.mx", string = "Correo del paciente", help = "Escriba el correo electronico del paciente")

    # informacion de pago
    patient_payment_mode = fields.Selection([('a','Efectivo'),('b','tarjeta de debito'),('c','Tarjeta de credito')], string = 'Metodo de pago' , default = 'a')
    
    @api.model
    def create(self, vals):
        if vals.get('patient_id', _('New')) == _('New'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('hospital.patient.order') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

