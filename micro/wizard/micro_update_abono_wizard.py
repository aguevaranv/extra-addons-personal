# -*- coding: utf-8 -*-

from odoo import fields, models, api


class UpdateAbonoWizard(models.TransientModel):
    _name = "micro.update.abono.wizard"

    name = fields.Char(string='Código', required=True, readonly=True, copy=False, default='New')
    idFactura = fields.Many2one(
        'micro.ticket', 
        string='Factura', 
        default=lambda self: self.env['micro.ticket'].search([('id', '=', self._context['active_id'])])
    )
    fch_Movimiento = fields.Datetime(string='Fecha', default=fields.Datetime.now())
    seleccion_tipo = [('creacion', 'Creación'),('abono', 'Abono'),('cancelacion', 'Cancelación')]
    tipo = fields.Selection(seleccion_tipo, 'Tipo', default='abono', tracking=True, readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
    valor = fields.Monetary(string='Valor', default=lambda self: self.env['micro.ticket'].search([('id', '=', self._context['active_id'])]).saldo)


    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El código debe ser único')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('secuencia.micro.movimiento') or 'New'
        result = super(UpdateAbonoWizard, self).create(vals)
        return result
    
    def update_vista_general(self):
        ticket_obj = self.env['micro.ticket']
        ticket_id = ticket_obj.search([('id', '=', self._context['active_id'])])
        # ticket_id = ticket_obj.browse(self._context['active_id'])
        ticket_id.abono += self.valor
        ticket_id.saldo = ticket_id.total - ticket_id.abono