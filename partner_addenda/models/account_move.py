# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_order_reference = fields.Char(string="Order Reference", store=True,
                                   help='Specifies the purchase order reference (Buyer) that the invoice refers to.')
    
    x_order_reference_date = fields.Date(string='Order Date', store=True,
                                         help='Specifies the purchase order date (Buyer) that the invoice refers to.')
    x_additional_reference = fields.Char(string='Additional Reference', store=True,
                                         help='Aproval Number')
    x_delivery_reference = fields.Char(string='Delivery Reference', store=True,
                                       help='Folio number. Number issued by the buyer when he reviews the merchandise that is invoiced')
    x_delivery_reference_date = fields.Date(string='Delivery Date', store=True,
                                            help='Specifies the date the receipt folio number was assigned.')