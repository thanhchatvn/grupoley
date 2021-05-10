# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    property_warehouse_id = fields.Many2one(
        related="picking_type_id.warehouse_id",
        string=u"Almacén",
    )
