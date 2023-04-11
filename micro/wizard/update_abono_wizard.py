# -*- coding: utf-8 -*-

from odoo import fields, models, api


class UpdateAbonoWizard(models.TransientModel):
    _name = "update.abono.wizard"

    name = fields.Char(string='Código', required=True, readonly=True, copy=False, default='New')
    idFactura = fields.Many2one(
        'micro.ticket', 
        string='Factura', 
        #default=lambda self: self.env.user.employee_id,domain="[('company_id','=',reparto_id)]" 
    )
    fch_Movimiento = fields.Datetime(string='Fecha', default=fields.Datetime.now())
    seleccion_tipo = [('creacion', 'Creación'),('abono', 'Abono'),('cancelacion', 'Cancelación')]
    tipo = fields.Selection(seleccion_tipo, 'Tipo', default='creacion', tracking=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
    valor = fields.Monetary(string='Total')


    _sql_constraints = [
        ('name_unique', 'unique(name)', 'El código debe ser único')
    ]

    # Campo sequence
    mi_modelo_sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('secuencia.micro.movimiento') or 'New'
        result = super(UpdateAbonoWizard, self).create(vals)
        return result
    
    def update_vista_general(self):
        presupuesto_obj = self.env['micro.ticket']
        presupuesto_id = presupuesto_obj.search([('id', '=', self._context['active_id'])])
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.abono += self.valor
        presupuesto_id.saldo = presupuesto_id.saldo - presupuesto_id.abono