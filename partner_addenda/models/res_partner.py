# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    x_gln = fields.Char(string='GLN', store=True, help='Global Location Number')
    x_center = fields.Char(string='Center', store=True, help="Customer Store")
    x_partner_code = fields.One2many('res.partner.supplierinfo', 'name')
    x_product_info = fields.One2many('product.supplierinfo.sale', 'partner_name')
    x_edi_identification = fields.Char(string="Identificador EDI", store=True, help="Identificador EDI del contacto")