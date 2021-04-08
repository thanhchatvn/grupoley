# -*- coding: utf-8 -*-

from odoo import models, fields, api

class default_product_company_id(models.Model):
    _inherit = 'product.template'

    company_id = fields.Many2one('res.company', 'Company', index=1,
                                 default=lambda self: self.env.company)