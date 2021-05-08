# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
    * Se modificó el modelo de "mrp.production" para agregar un boton que nos permita consumir
      todos los insumos en la lista de materiales sin la necesidad de cambiar de etapa.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 08/04/2021
    *************************************************************************/
'''

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    x_is_cosume_all_clicked = fields.Boolean(string="Se ha clickeado el boton cosumir", default=False)

    def button_mark_done(self):
        if not self.x_is_cosume_all_clicked:
            error = "Se debe de consumir todos los insumos"
            raise UserError(error)
        res = super(MrpProduction, self).button_mark_done()
        return res

    def button_cosume_all(self):
        for production in self:
            error_msg = ""
            if production.product_tracking in ('lot', 'serial') and not production.lot_producing_id:
                production.action_generate_serial()
            if production.product_tracking == 'serial' and float_compare(production.qty_producing, 1,
                                                                         precision_rounding=production.product_uom_id.rounding) == 1:
                production.qty_producing = 1
            else:
                production.qty_producing = production.product_qty - production.qty_produced
            production._set_qty_producing()
            for move in production.move_raw_ids.filtered(lambda m: m.state not in ['done', 'cancel']):
                rounding = move.product_uom.rounding
                for move_line in move.move_line_ids:
                    if move_line.product_uom_qty:
                        move_line.qty_done = min(move_line.product_uom_qty, move_line.move_id.should_consume_qty)
                    if float_compare(move.quantity_done, move.should_consume_qty, precision_rounding=rounding) >= 0:
                        self.x_is_cosume_all_clicked = True
                        break
                if float_compare(move.product_uom_qty, move.quantity_done,
                                 precision_rounding=move.product_uom.rounding) == 1:
                    if move.has_tracking in ('serial', 'lot'):
                        error_msg += "\n  - %s" % move.product_id.display_name

            if error_msg:
                error_msg = _('You need to supply Lot/Serial Number for products:') + error_msg
                raise UserError(error_msg)

