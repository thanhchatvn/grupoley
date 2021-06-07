# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockSerial(models.Model):
    _inherit = 'stock.production.lot'

    x_stock_quant = fields.One2many('stock.quant', 'lot_id', string="Existencias de inventario")
