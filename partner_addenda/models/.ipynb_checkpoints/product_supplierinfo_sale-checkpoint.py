# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductSupplierinfoSale(models.Model):
    _name = 'product.supplierinfo.sale' 
    _description = 'Relation between product info from customer'
    
    partner_name = fields.Many2one('res.partner', ondelete='cascade', requered=True)
    product_name = fields.Many2one('product.template', ondelete='cascade', required=True)     
    product_code = fields.Char(string='Product code', help='Code that customer know the product')
    uom = fields.Char(string='UOM', help='Unit Of Measurement')
    uom_additional = fields.Char(string='UOM Additional', help='Unit Of Measurement Additional')
    company = fields.Many2one('res.company','Company', default=lambda self: self.env.company)
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    x_product_supplierinfo = fields.One2many('product.supplierinfo.sale', 'product_name')