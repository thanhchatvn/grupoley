# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
      Se modifico el módelo de 'stock.valuation.layer' para modificar la forma en que se agrupa el campo
      haciendo que no aparezca en el encabezado la suma de los valores de la columna
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 22/04/2021
    *************************************************************************/
'''

from odoo import models, fields, api


class StockValuationUnitValue(models.Model):
    _inherit = 'stock.valuation.layer'

    unit_cost = fields.Monetary('Unit Value', readonly=True, group_operator=False)