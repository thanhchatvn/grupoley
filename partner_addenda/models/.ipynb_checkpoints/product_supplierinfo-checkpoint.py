# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'
    
    x_customer_seller = fields.Char(string="Customer/Seller", store=True,
                                    help="Name with which our company is identified by the customer.")
    
    x_center = fields.Char(string='Center', store=True, help="Customer Store")
    x_uom = fields.Char(string='UOM', store=True, help='Unit Of Measurement')