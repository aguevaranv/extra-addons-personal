# -*- coding: utf-8 -*-

import logging

from odoo.exceptions import ValidationError
from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class Factura(models.Model):
    _name = "micro.factura"
    _inherit = ['image.mixin']

    # @api.depends('detalle_ids')
    # def _compute_total(self):
    #     for rcord in self:
    #         sub_total = 0
    #         for linea in rcord.detalle_ids:
    #             sub_total += linea.importe
    #         rcord.base = sub_total
    #         rcord.impuestos = sub_total * 0.12
    #         rcord.total = sub_total * 1.12


    name = fields.Char(string="Factura No.", readonly=True, select=True, copy=False, default='Nueva') #-----campo caracter muestra el string en la vista, nombre principal
    nombre = fields.Char(string='Nombres')
    cedula = fields.Char(string='CI')
    fch_factura = fields.Datetime(string='Fecha creacion', copy=False, default=lambda self: fields.Datetime.now())

    #relacion con los detalles relacion One2many
    detalle_ids = fields.One2many(
        comodel_name='micro.factura.detalle',
        #relacion del detalle con la cabecera
        inverse_name='factura_id',
        string='Detalles',
    )
    campos_ocultos = fields.Boolean(string='Campos ocultos')


    def aprobar_factura(self):
        logger.info('Entro a la funcion aprobar factura')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_factura(self):
        logger.info('Entro a la funcion aprobar factura')
        self.state = 'cancelado'

    def unlink(self):
        logger.info('********Se disparo la funcion unlink')
        for record in self:
            if record.state != 'cancelado':
                raise UserError('Solo se eliminan registros con estado cancelado')
            super(Factura, record).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nueva') == 'Nueva':
            vals['name'] = self.env['ir.sequence'].next_by_code('secuencia.micro.factura') or 'New'
            #raise ValidationError(vals['name'])
        return super(Factura, self).create(vals)


    def write(self, variables):
        logger.info('******** variables: {0}'.format(variables))
        if 'clasificacion' in variables:
            raise UserError('La clasificacion no se puede editar')
        return super(Factura, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        default['puntuacion2'] = 1
        return super(Factura, self).copy(default)

    @api.onchange('clasificacion')
    def _onchage_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = 'Publico general'
            if self.clasificacion == 'PG':
                self.dsc_clasificacion = 'Se recomienda la compania de un adulto'
            if self.clasificacion == 'PG-13':
                self.dsc_clasificacion = 'Mayores de 13 años'
            if self.clasificacion == 'R':
                self.dsc_clasificacion = 'En compania de un adulto obligatorio'
            if self.clasificacion == 'NC-17':
                self.dsc_clasificacion = 'Mayores de 18'
        else:
            self.dsc_clasificacion = False

class FacturaDetalle(models.Model):
    _name = "micro.factura.detalle"
    
    factura_id = fields.Many2one(
        comodel_name='micro.factura',
        string='Factura',
    )
    name = fields.Many2one(
        comodel_name='micro.servicio', #debe listar los productos del modelo product.product
        string='Servicio',
    )
    descripcion = fields.Char(string='Descripcion',related='name.descripcion')
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        related='name.contacto_id'
    )
    imagen = fields.Binary(string='Imagen',related='name.imagen')
    cantidad = fields.Float(string='Cantidad', default=1.0, digits=(16, 4))
    precio = fields.Float(string='Precio', digits='Product Price')
    importe = fields.Float(string='Importe')#fields.Monetary(string='Importe')

#     # currency_id = fields.Many2one(
#     #     comodel_name='res.currency',
#     #     string='Moneda',
#     #     related='factura_id.currency_id'
#     # )
    

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio

    
    @api.onchange('cantidad', 'precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio