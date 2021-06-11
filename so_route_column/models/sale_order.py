# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderLineRouteColumn(models.Model):
    _inherit = 'sale.order.line'

    product_route_id = fields.Many2one( "stock.location.route", string="Ruta")
  
    @api.onchange('product_route_id','product_id')
    def _domain_product_route_id_onchange(self):
        return {'domain': {'product_route_id': [('id', 'in', self.product_id.route_ids.ids)]}}