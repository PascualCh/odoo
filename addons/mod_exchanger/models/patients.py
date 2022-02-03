from ast import Str
from email.policy import default
from pickle import FALSE
import string
from tokenize import String
from odoo import models,fields



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient record'

    #agregar campos flotantes, enteros, tipo seleccion, boleanos
    #agregar en los parametros de creacion default,readonly,required, help
    
    patient_name = fields.Char(dafult = "Pedro", string = "Nombre paciente", help = "Nombre del paciente", required = True)
    patient_state = fields.Boolean(default = False, string = "Vivo ", help = "Estado del paciente", required = True)
    patient_height = fields.Float(default = 1.75, string = "Estatura", help = "Estatura del paciente", required = False)
    patient_id = fields.Char(default = "M12358", string = "Matricula del paciente", readonly = True)
    patient_grade = fields.Selection([('a','sin seguro'),('b','con seguro'),('c','Premium')], string = 'Tipo de paciente' , default = 'a')
    patient_photo = fields.Binary( String = "Foto", )
