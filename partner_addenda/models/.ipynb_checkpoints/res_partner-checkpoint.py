# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    x_gln = fields.Char(string='GLN', store=True, help='Global Location Number')
    x_center = fields.Char(string='Center', store=True, help="Customer Store")
    x_partner_code = fields.One2many('res.partner.supplierinfo', 'name')