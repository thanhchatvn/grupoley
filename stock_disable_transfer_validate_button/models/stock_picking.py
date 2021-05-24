# -*- coding: utf-8 -*-

from odoo import fields,models,api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    x_is_same_location = fields.Boolean(string="Misma ubicacion de usuario y destino",
                                        compute="_is_same_location")

    @api.onchange('location_dest_id')
    def _is_same_location(self):
        user = self.env.user
        print(user.name)
        print(user.property_warehouse_id.lot_stock_id)
        for rec in self:
            print(rec.location_dest_id)
            if (user.property_warehouse_id.lot_stock_id and rec.location_dest_id
                and rec.picking_type_id.code == 'internal'):
                if user.property_warehouse_id.lot_stock_id == rec.location_dest_id:
                    rec.x_is_same_location = True
                else:
                    rec.x_is_same_location = False
            else:
                rec.x_is_same_location = False

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for picking in self:
            if picking.picking_type_code == 'internal' and picking.x_is_same_location:
                raise UserError('No puedes validar debido a que perteneces a la misma bodega que solicita')
        return res