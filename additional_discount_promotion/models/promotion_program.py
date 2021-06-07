# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
    * Se agregó un campo nuevo a las promociones para poder realizar un descuento en cascada, adicional al
      descuento que se tiene actualmente que puede ser una suma directa al campo de descuento en la linea
      de pedido
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 07/06/2021
    *************************************************************************/
'''

from odoo import models, fields, api
from itertools import groupby

class CouponReward(models.Model):
    _inherit = 'coupon.reward'

    reward_type = fields.Selection([
        ('discount', 'Discount'),
        ('multi_discount', 'Descuento en cascada'),
        ('product', 'Free Product'),
        ('same_product', 'Mismo Producto Gratis'),

    ], string='Reward Type', default='discount',
        help="Discount - Reward will be provided as discount.\n" +
             "Free Product - Free product will be provide as reward \n" +
             "Free Shipping - Free shipping will be provided as reward (Need delivery module)")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Se agregó la condición de si el tipo de descuento es multi_discount
    def _custom_create_new_no_code_promo_reward_lines(self):
        '''Apply new programs that are applicable'''
        self.ensure_one()
        order = self

        programs = order._get_applicable_no_code_promo_program()
        programs = programs._keep_only_most_interesting_auto_applied_global_discount_program()
        for program in programs:
            # VFE REF in master _get_applicable_no_code_programs already filters programs
            # why do we need to reapply this bunch of checks in _check_promo_code ????
            # We should only apply a little part of the checks in _check_promo_code...
            error_status = program._check_promo_code(order, False)
            #if not error_status.get('error') or program.reward_type == 'discount':
            if program.promo_applicability == 'on_next_order':
                order._create_reward_coupon(program)
            #elif program.discount_line_product_id.id not in self.order_line.mapped('product_id').ids:
            elif program.reward_type == 'discount':
                self._get_custom_reward_values_discount(program)
            elif program.reward_type == 'multi_discount':
                self._get_custom_reward_values_multi_discount(program)
            elif program.reward_type == 'product':
                self.write({'order_line': [(0, False, value) for value in self._get_custom_reward_line_values(program, 0)]})

            elif program.reward_type == 'same_product':
                #agrupar por producto y sumar la cantidad
                order_lines = (self.order_line - self._get_reward_lines()).filtered(lambda x: program._get_valid_products(x.product_id))
                for key in groupby(sorted(order_lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id):
                    program.write({'reward_product_id': key[0],'discount_line_product_id': key[0]})
                    self.write({'order_line': [(0, False, value) for value in self._get_custom_reward_line_values(program, key[0])]})

                #order_lines = self.order_line
                """for order_line in order_lines:
                    program.write({'reward_product_id': order_line.product_id.id, 'discount_line_product_id': order_line.product_id.id})
                    self.write({'order_line': [(0, False, value) for value in self._get_custom_reward_line_values(program, order_line.product_id.id)]})"""

            order.no_code_promo_program_ids |= program


    # Si el descuento es de tipo multi_discount se añade un descuento en cascada
    def _get_custom_reward_values_multi_discount(self, program):
        order = self
        for line in order.order_line:
            if order._is_valid_product(program, line) and not line.is_reward_line:
                tmp_discount_sum = program.discount_percentage + line.discount_original
                if (line.is_discount_calculated and line.discount == tmp_discount_sum):
                    line.write({'discount_original': line.discount_original, 'discount_rate': line.discount_original})
                else:
                    line.write({'discount_original': line.discount, 'discount_rate': line.discount,
                                'is_discount_calculated': True})

                line.write({'discount_promotions': program.discount_percentage})
                discount_amount = line.price_unit * line.product_uom_qty * (line.discount_rate / 100)
                price_with_discount = line.price_unit - discount_amount
                additional_discount_amount = price_with_discount * (line.discount_promotions / 100)
                price_with_additional_discount = price_with_discount - additional_discount_amount
                additional_dicount = (price_with_discount - price_with_additional_discount) * 100 / line.price_unit
                discount_sum = line.discount_rate + additional_dicount
                line.write({'discount': discount_sum})
        return line



