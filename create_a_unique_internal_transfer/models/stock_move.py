# -*- coding: utf-8 -*-

'''
    /*************************************************************************
    * Description
    * Se modificó el metodo "_assingn_picking" del modelo stock_move con la finalidad de crear odernes
      de transferencia diferentes cada vez que se crea una orden de producción.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 12/06/2021
    *************************************************************************/
'''

from odoo import models, fields, api
from itertools import groupby

class StockMove(models.Model):
    _inherit = "stock.move"

    def _assign_picking(self):
        Picking = self.env['stock.picking']
        grouped_moves = groupby(sorted(self, key=lambda m: [f.id for f in m._key_assign_picking()]), key=lambda m: [m._key_assign_picking()])
        for group, moves in grouped_moves:
            moves = self.env['stock.move'].concat(*list(moves))
            new_picking = True
            picking = Picking.create(moves._get_new_picking_values())
            moves.write({'picking_id': picking.id})
            moves._assign_picking_post_process(new=new_picking)
        return True