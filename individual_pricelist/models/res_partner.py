# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def _commercial_fields(self):
        res = super(Partner, self)._commercial_fields()
        res.remove('property_product_pricelist')
        return res





