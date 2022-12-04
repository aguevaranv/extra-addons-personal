# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Alumno(models.Model):
    _name = 'estudiantil.alumno'
    _description = 'Alumno'
    _rec_name = 'nombre'   
    
    
    cedula = fields.Char( string='Cédula',size=10, required=True, default="0000000000")    
    edad = fields.Integer(string='Edad',)        
    nombre = fields.Char(string='Nombres y apellidos',)    
    
    
    
    
    
    
   