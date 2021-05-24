# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class PosAutorizacion(models.Model):
    _name = "pos.autorizacion"
    _order = "create_date desc, name desc"

    def _compute_tot(self):
        for record in self:
            subtotal_sin_impuestos = 0
            subtotal_con_impuestos = 0
            for linea in record.detalle_ids:
                subtotal_sin_impuestos += linea.subtotal_sin_impuestos
                subtotal_con_impuestos += linea.subtotal_con_impuestos
            record.tot_impuestos = subtotal_con_impuestos - subtotal_sin_impuestos
            record.tot = subtotal_con_impuestos

    name = fields.Char(string=u'Número de recibo')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Cajero'
    )
    autorizador_id = fields.Many2one(
        comodel_name='res.users',
        string='Autorizador'
    )
    state = fields.Selection(selection=[
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ], default='pendiente', string='Estado')
    detalle_ids = fields.One2many(
        comodel_name='pos.autorizacion.line',
        inverse_name='autorizacion_id',
        string='Detalles'
    )
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Lista de Precios',
    )
    tot_impuestos = fields.Float(string='Impuestos', digits=0, compute='_compute_tot')
    tot = fields.Float(string='Total', digits=0, compute='_compute_tot')
    currency_id = fields.Many2one(
        related='pricelist_id.currency_id',
        string='Moneda',
    )
    motivo = fields.Text(string='Motivo')

    def revisar_estado(self):
        return self.state

    def aprobar(self):
        self.state = 'aprobado'
        self.autorizador_id = self.env.user

    def rechazar(self):
        self.state = 'rechazado'
        self.autorizador_id = self.env.user

    def comprobar(self, data):
        if self.partner_id.id != data['partner_id']:
            return False
        if self.pricelist_id.id != data['pricelist_id']:
            return False
        for num, linea in enumerate(self.detalle_ids):
            if linea.product_id.id != data['detalles'][num][0]['product_id']:
                return False
            if linea.cantidad != data['detalles'][num][0]['cantidad']:
                return False
            if linea.unitario != data['detalles'][num][0]['unitario']:
                return False
            if linea.descuento != data['detalles'][num][0]['descuento']:
                return False
        return True


class PosAutorizacionLine(models.Model):
    _name = "pos.autorizacion.line"

    autorizacion_id = fields.Many2one(
        comodel_name='pos.autorizacion',
        string=u'Autorización'
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Producto'
    )
    cantidad = fields.Float(string='Cantidad')
    unitario = fields.Monetary(string='Precio unitario')
    descuento = fields.Float(string='Desc.%')
    impuesto = fields.Many2many(
        comodel_name='account.tax',
        string='Impuestos'
    )
    subtotal_sin_impuestos = fields.Monetary(string='Subtotal neto')
    subtotal_con_impuestos = fields.Monetary(string='Subtotal')
    currency_id = fields.Many2one(
        related='autorizacion_id.currency_id',
        string='Moneda'
    )

    def _onchange_qty(self):
        if self.product_id:
            if not self.autorizacion_id.pricelist_id:
                raise UserError('Debe seleccionar una lista de precios.')
            price = self.unitario * (1 - (self.descuento or 0.0) / 100.0)
            self.subtotal_sin_impuestos = self.subtotal_con_impuestos = price * self.cantidad
            if (self.product_id.taxes_id):
                taxes = self.product_id.taxes_id.compute_all(price, self.autorizacion_id.pricelist_id.currency_id, self.cantidad,
                                                             product=self.product_id, partner=False)
                self.subtotal_sin_impuestos = taxes['total_excluded']
                self.subtotal_con_impuestos = taxes['total_included']

    @api.model
    def create(self, vals):
        res = super(PosAutorizacionLine, self).create(vals)
        res._onchange_qty()
        return res
