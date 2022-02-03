from attr import field
from odoo import fields, models

class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"

    name = fields.Char("Name")
    status = fields.Selection(selection = [("borrador", "Borrador") ("hecho","Hecho")])

