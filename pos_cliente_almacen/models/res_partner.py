# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_warehouse_id = fields.Many2one(
        related="user_id.property_warehouse_id",
        string=u"Almacén",
    )