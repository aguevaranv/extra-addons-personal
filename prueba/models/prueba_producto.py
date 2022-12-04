# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Producto(models.Model):
    _name = 'prueba.producto'
    _description = 'Producto'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombres producto',)
    stock = fields.Integer(string='Stock',)        
