# -*- coding: utf-8 -*-

from odoo import models, fields, api


class partner_addenda(models.Model):
    _inherit = 'sale.order'

    x_order_reference_date = fields.Date(string='Order Date', store=True,
                                         help='Specifies the purchase order date (Buyer) that the invoice refers to.')
    x_additional_reference = fields.Char(string='Additional Reference', store=True,
                                         help='Aproval Number')
    x_delivery_reference = fields.Char(string='Delivery Reference', store=True,
                                       help='Folio number. Number issued by the buyer when he reviews the merchandise that is invoiced')
    x_delivery_reference_date = fields.Date(string='Delivery Date', store=True,
                                            help='Specifies the date the receipt folio number was assigned.')