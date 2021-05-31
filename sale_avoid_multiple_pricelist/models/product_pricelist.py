# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.constrains('item_ids')
    def _check_item_ids(self):
        products = []
        for object in self:
            for item in object.item_ids:
                if item.name not in products:
                    products.append(item.name)
                else:
                    raise UserError(_("No es posible añadir el mismo producto en una tarifa, el producto  \" %s \"  está duplicado" % item.name))