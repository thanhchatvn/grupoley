# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    desc_pos = fields.Boolean(string='Desc. POS')

    def unlink(self):
        for record in self:
            if record.desc_pos:
                raise UserError('No se puede eliminar este producto')
        return super(ProductTemplate, self).unlink()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    desc_pos = fields.Boolean(
        related='product_tmpl_id.desc_pos',
        string='Desc. POS',
        store=True,
    )

    def unlink(self):
        for record in self:
            if record.desc_pos:
                raise UserError('No se puede eliminar este producto')
        return super(ProductProduct, self).unlink()