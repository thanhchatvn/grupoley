# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerSupplierinfo(models.Model):
    _name = 'res.partner.supplierinfo'
    _description = 'Indlude additional information about partner'
    
    name = fields.Many2one(
        'res.partner',
        ondelete='cascade', required=True)
    companies = fields.Many2one('res.company','Company', default=lambda self: self.env.company)
    code = fields.Char(string='Seller code')
    
    