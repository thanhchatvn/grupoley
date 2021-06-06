# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    @api.model
    def create(self, vals):
        program = super().create(vals)
        if not vals.get('discount_line_product_id', False):
            program.discount_line_product_id.unlink()
            program.update({'discount_line_product_id': program.reward_product_id})
            discount_line_product_id = program.reward_product_id
            program.write({'discount_line_product_id': discount_line_product_id.id})
        return program

    @api.onchange('reward_product_id')
    def _update_discount_line_product_id(self):
        self.discount_line_product_id = self.reward_product_id and self.reward_product_id.id or False
