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

    def recompute_coupon_lines(self):
        for order in self:
            order._custom_remove_invalid_reward_lines()
            order._custom_create_new_no_code_promo_reward_lines()
            order._custom_update_existing_reward_lines()

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
            # if not error_status.get('error') or program.reward_type == 'discount':
            if program.promo_applicability == 'on_next_order':
                order._create_reward_coupon(program)
            # elif program.discount_line_product_id.id not in self.order_line.mapped('product_id').ids:
            elif program.reward_type == 'discount':
                self._get_custom_reward_values_discount(program)
            elif program.reward_type == 'multi_discount':
                self._get_custom_reward_values_multi_discount(program)
            elif program.reward_type == 'product':
                self.write(
                    {'order_line': [(0, False, value) for value in self._get_custom_reward_line_values(program, 0)]})
            elif program.reward_type == 'same_product':
                # agrupar por producto y sumar la cantidad
                order_lines = (self.order_line - self._get_reward_lines()).filtered(
                    lambda x: program._get_valid_products(x.product_id))
                for key in groupby(sorted(order_lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id):
                    program.write({'reward_product_id': key[0], 'discount_line_product_id': key[0]})
                    self.write({'order_line': [(0, False, value) for value in
                                               self._get_custom_reward_line_values(program, key[0])]})

                # order_lines = self.order_line
                """for order_line in order_lines:
                    program.write({'reward_product_id': order_line.product_id.id, 'discount_line_product_id': order_line.product_id.id})
                    self.write({'order_line': [(0, False, value) for value in self._get_custom_reward_line_values(program, order_line.product_id.id)]})"""

            order.no_code_promo_program_ids |= program


    def _custom_update_existing_reward_lines(self):
        '''Update values for already applied rewards'''

        def update_line(order, lines, values):
            '''Update the lines and return them if they should be deleted'''
            lines_to_remove = self.env['sale.order.line']
            # Check commit 6bb42904a03 for next if/else
            # Remove reward line if price or qty equal to 0
            if values['product_uom_qty'] and values['price_unit']:
                lines.write(values)
            else:
                if program.reward_type != 'free_shipping':
                    # Can't remove the lines directly as we might be in a recordset loop
                    lines_to_remove += lines
                else:
                    values.update(price_unit=0.0)
                    lines.write(values)
            return lines_to_remove

        self.ensure_one()
        order = self
        applied_programs = order._get_applied_programs_with_rewards_on_current_order()

        for program in applied_programs:
            values = order._get_custom_reward_line_values(program, 0)
            lines = order.order_line.filtered(lambda line: line.product_id == program.discount_line_product_id)
            if not lines:
                return False
            if program.reward_type == 'multi_discount' and program.discount_type == 'percentage':
                lines_to_remove = lines
                # Values is what discount lines should really be, lines is what we got in the SO at the moment
                # 1. If values & lines match, we should update the line (or delete it if no qty or price?)
                # 2. If the value is not in the lines, we should add it
                # 3. if the lines contains a tax not in value, we should remove it
                for value in values:
                    value_found = False
                    for line in lines:
                        # Case 1.
                        if not len(set(line.tax_id.mapped('id')).symmetric_difference(
                                set([v[1] for v in value['tax_id']]))):
                            value_found = True
                            # Working on Case 3.
                            lines_to_remove -= line
                            lines_to_remove += update_line(order, line, value)
                            continue
                    # Case 2.
                    if not value_found:
                        order.write({'order_line': [(0, False, value)]})

                # Case 3.
                lines_to_remove.unlink()
            elif program.reward_type == 'discount' and program.discount_type == 'percentage':
                lines_to_remove = lines
                # Values is what discount lines should really be, lines is what we got in the SO at the moment
                # 1. If values & lines match, we should update the line (or delete it if no qty or price?)
                # 2. If the value is not in the lines, we should add it
                # 3. if the lines contains a tax not in value, we should remove it
                for value in values:
                    value_found = False
                    for line in lines:
                        # Case 1.
                        if not len(set(line.tax_id.mapped('id')).symmetric_difference(
                                set([v[1] for v in value['tax_id']]))):
                            value_found = True
                            # Working on Case 3.
                            lines_to_remove -= line
                            lines_to_remove += update_line(order, line, value)
                            continue
                    # Case 2.
                    if not value_found:
                        order.write({'order_line': [(0, False, value)]})

                # Case 3.
                lines_to_remove.unlink()
            # else:
            #    update_line(order, lines, values[0]).unlink()

    # Si el descuento es de tipo multi_discount se añade un descuento en cascada
    def _get_custom_reward_values_multi_discount(self, program):
        order = self
        for line in order.order_line:
            if order._is_valid_product(program, line) and not line.is_discount_calculated and line.price_unit > 0:
                tmp_discount_sum = program.discount_percentage + line.discount_original
                if line.is_discount_calculated:
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
                line.is_reward_line == True
        return line
