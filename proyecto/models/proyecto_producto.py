# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Producto(models.Model):
    _name = 'proyecto.producto'
    _description = 'Producto'

    nombre = fields.Char(string='Nombres producto',)
    stock = fields.Integer(string='Stock',)    


