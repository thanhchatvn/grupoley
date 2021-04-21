# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    x_order_reference = fields.Char(string='Folio de Orden de Compra')
    x_order_reference_date = fields.Date(string='Fecha de Orden de Compra')
    x_delivery_reference = fields.Char(string='Folio de Entrega')
    x_delivery_reference_date = fields.Date(string='Fecha de Entrega')