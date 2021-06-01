# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
      - Se agregaron campos de categoria de producto en el modelo 'stock.quant'
        para poder realizar la union de aquellas tablas en el query.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 26/04/2021
    *************************************************************************/
'''

from odoo import models, fields, api, tools

class report_stock_quantity_custom(models.Model):
    _inherit = 'stock.quant'

    x_product_category = fields.Many2one(related="product_id.product_tmpl_id.categ_id",
                                         store=True, readonly=True)