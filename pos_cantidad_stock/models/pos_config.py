# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    default_location_src_id = fields.Many2one(
        related="picking_type_id.default_location_src_id",
        string=u"Ubicación",
    )
