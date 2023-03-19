# -*- coding: utf-8 -*-

import logging

from odoo import fields, models, api

class MicroServicio(models.Model):
    _name = "micro.servicio"

    name = fields.Char(string='Sevicio')
    descripcion = fields.Char(string='Descripcion')
    precio = fields.Float(string='Precio')
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        domain="[('is_company', '=', False)]"
    )
    imagen = fields.Binary(string='Imagen')