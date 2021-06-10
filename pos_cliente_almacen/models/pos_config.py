# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    property_warehouse_id = fields.Many2one(
        related="picking_type_id.warehouse_id",
        string=u"Almacén",
    )

    check_all_client_picking_type = fields.Boolean(default=False, string="Habilitar todos los clientes")