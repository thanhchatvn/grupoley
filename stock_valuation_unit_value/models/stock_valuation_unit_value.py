# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockValuationUnitValue(models.Model):
    _inherit = 'stock.valuation.layer'

    unit_cost = fields.Monetary('Unit Value', readonly=True, group_operator=False)