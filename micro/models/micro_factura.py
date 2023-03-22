# -*- coding: utf-8 -*-

import logging
import re

from odoo.exceptions import ValidationError
from odoo import fields, models, api
from odoo.exceptions import UserError, Warning

logger = logging.getLogger(__name__)

class Factura(models.Model):
    _name = "micro.factura"
    _inherit = ['image.mixin']

    @api.depends('detalle_ids') #depends es para que la funcion se ejecute cada vez que cambie detalle_ids o se renderice la vista por compute
    def _compute_total(self):
        for rcord in self:
            sub_total = 0
            for linea in rcord.detalle_ids:
                sub_total += linea.importe
            rcord.base = sub_total
            rcord.impuestos = 0
            rcord.total = sub_total + rcord.impuestos


    name = fields.Char(string="Factura No.", readonly=True, select=True, copy=False, default='Nueva') #-----campo caracter muestra el string en la vista, nombre principal
    nombre = fields.Many2one(
        'res.partner', 
        string='Cliente', 
        #default=lambda self: self.env.user.employee_id,domain="[('company_id','=',reparto_id)]" 
    )
    identificacion = fields.Char(string='ID', size=13)
    fch_factura = fields.Datetime(string='Fecha creacion', copy=False)

    #relacion con los detalles relacion One2many
    detalle_ids = fields.One2many(
        comodel_name='micro.factura.detalle',
        #relacion del detalle con la cabecera
        inverse_name='factura_id',
        string='Detalles',
    )
    campos_ocultos = fields.Boolean(string='Campos ocultos')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
    terminos = fields.Text(string='Terminos')
    base = fields.Monetary(string='Base imponible', compute='_compute_total')
    impuestos = fields.Monetary(string='Impuestos', compute='_compute_total')
    total = fields.Monetary(string='Total')
    abono = fields.Monetary(string='Abono')
    saldo = fields.Monetary(string='Saldo')

    @api.onchange('total', 'abono')
    def _onchange_saldo(self):
        self.saldo = self.total - self.abono

    @api.onchange('nombre')
    def _onchange_nombre_cliente(self):
        self.identificacion = self.nombre.vat
    
    @api.onchange('identificacion')
    def _onchange_id(self):
        if self.identificacion:
            if self.env['res.partner'].search([('vat','=',self.identificacion)],limit=1):
                    self.nombre = self.env['res.partner'].search([('vat','=',self.identificacion)],limit=1)
            else:
                self.nombre = False
        else:
            self.nombre = False

    @api.constrains('identificacion')
    def _check_identificacion_cliente(self):
        if self.identificacion:
            if not re.match(r'^\d{10}',self.identificacion) and not re.match(r'^\d{13}',self.identificacion) or not self.identificacion.isdigit():
                raise UserError('Error en identificación')

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
            # if record.state != 'cancelado':
            #     raise UserError('Solo se eliminan registros con estado cancelado')
            super(Factura, record).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nueva') == 'Nueva':
            vals['name'] = self.env['ir.sequence'].next_by_code('secuencia.micro.factura') or 'New'
            vals['fch_factura'] = fields.Datetime.now()
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
    importe = fields.Monetary(string='Importe') #depende de currency_id

    #Para que funcione Monetary
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        related='factura_id.currency_id'
    )
    

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio

    
    @api.onchange('cantidad', 'precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio