# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_delivery_note_acc(models.Model):
    _inherit = "stock.picking"
    
    # Campo Remision que representa un tipo de documento emitido por el proveedor para validar que el pedido o parte del
    #pedido ha sido recibido
    x_remis = fields.Char('Remision',
                                help='Document type from provider to validate a delivery slip')

    



    
