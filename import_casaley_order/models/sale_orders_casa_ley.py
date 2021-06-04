# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class SaleOrdersCasaLey(models.Model):
    _name = 'sale.orders.casa.ley'
    _description = 'Ordenes de compra de Casa Ley'

    name = fields.Char(string='Folio de orden', store=True)
    partner_id = fields.Many2one('res.partner',string='Cliente', store=True)
    user_id = fields.Many2one(related='partner_id.user_id', string='Comercial',
                              store=True)
    payment_term_id = fields.Many2one(related='partner_id.property_payment_term_id',
                                      store=True)
    warehouse_id = fields.Many2one(related='partner_id.user_id.property_warehouse_id',
                                   store=True)
    date_order = fields.Date(string='Fecha', store=True, readonly=True)
    import_id = fields.Many2one('import.ley.order', string='Interfaz de pedido',
                                store=True)
    order_lines = fields.One2many('sale.orders.casa.ley.line','sale_order_id')
    
    zone = fields.Many2one(related='partner_id.x_zone', string='Territorio', store=True)

class SaleOrderCasaLeyLine(models.Model):
    _name = 'sale.orders.casa.ley.line'
    _description = 'Lineas de orden de compra de Casa Ley'

    name = fields.Char(string='Descripción', store=True)
    product_id = fields.Many2one('product.product', string='Producto', store=True)
    qty_uom = fields.Float(string='Cantidad solicitada', store=True)
    sale_order_id = fields.Many2one('sale.orders.casa.ley', string='Linea de pedido',
                                    store=True, readonly=True)
    route_id = fields.Many2one('stock.location.route', string='Ruta')