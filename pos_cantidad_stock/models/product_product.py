# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def prueba(self, location):
        consolidado = []
        quant_ids = self.env['stock.quant'].search([
            ('location_id', '=', location),
        ])
        product_ids = self.env['product.product'].search([
            ('available_in_pos', '=', True),
        ])
        for product_id in product_ids:
            if product_id in quant_ids.product_id:
                consolidado.append({
                    'id': product_id.id,
                    'qty_available': quant_ids.filtered(lambda x: x.product_id == product_id).quantity,
                })
            else:
                consolidado.append({
                    'id': product_id.id,
                    'qty_available': 0,
                })
        return consolidado