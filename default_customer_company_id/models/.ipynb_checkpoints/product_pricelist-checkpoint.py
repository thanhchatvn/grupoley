# -*- coding: utf-8 -*-

from odoo import models, fields, api

class default_product_company_id(models.Model):
    _inherit = 'product.pricelist'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)


