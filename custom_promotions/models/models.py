# -*- coding: utf-8 -*-
import ast

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    is_promo = fields.Boolean(default=False, string="¿es promo?")

    discount_rate = fields.Float()
    discount_promotions = fields.Float()
    is_discount_calculated = fields.Boolean()
    discount_original = fields.Float()




class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    """reward_type = fields.Selection([
        ('discount', 'Discount'),
        ('product', 'Free Product'),
        ('same_product', 'Mismo Producto gratis'),
    ], string='Reward Type', default='discount',
        help="Discount - Reward will be provided as discount.\n" +
             "Free Product - Free product will be provide as reward \n" +
             "Free Shipping - Free shipping will be provided as reward (Need delivery module)")"""

    @api.model
    def _filter_programs_from_common_rules(self, order, next_order=False):
        """ Return the programs if every conditions is met
            :param bool next_order: is the reward given from a previous order
        """
        programs = self
        # Minimum requirement should not be checked if the coupon got generated by a promotion program (the requirement should have only be checked to generate the coupon)
        if not next_order:
            programs = programs and programs._filter_on_mimimum_amount(order)
        if not self.env.context.get("no_outdated_coupons"):
            programs = programs and programs._filter_on_validity_dates(order)
        programs = programs and programs._filter_unexpired_programs(order)
        programs = programs and programs._filter_programs_on_partners(order)
        # Product requirement should not be checked if the coupon got generated by a promotion program (the requirement should have only be checked to generate the coupon)
        if not next_order:
            programs = programs and programs._filter_programs_on_products(order)

        programs_curr_order = programs.filtered(lambda p: p.promo_applicability == 'on_current_order')
        programs = programs.filtered(lambda p: p.promo_applicability == 'on_next_order')
        if programs_curr_order:
            # Checking if rewards are in the SO should not be performed for rewards on_next_order
            programs += programs_curr_order._filter_not_ordered_reward_programs(order)
        return programs



    def _filter_not_ordered_reward_programs(self, order):
        """
        Returns the programs when the reward is actually in the order lines
        """
        programs = self.env['coupon.program']
        for program in self:
            """if program.reward_type == 'product' and \
               not order.order_line.filtered(lambda line: line.product_id == program.reward_product_id):
                continue
            el"""
            if program.reward_type == 'discount' and program.discount_apply_on == 'specific_products' and \
               not order.order_line.filtered(lambda line: line.product_id in program.discount_specific_product_ids):
                continue
            programs |= program
        return programs

    def _filter_programs_on_products(self, order):
        """
        To get valid programs according to product list.
        i.e Buy 1 imac + get 1 ipad mini free then check 1 imac is on cart or not
        or  Buy 1 coke + get 1 coke free then check 2 cokes are on cart or not
        """
        order_lines = order.order_line.filtered(lambda line: line.product_id) - order._get_reward_lines()
        products = order_lines.mapped('product_id')
        products_qties = dict.fromkeys(products, 0)
        for line in order_lines:
            products_qties[line.product_id] += line.product_uom_qty
        valid_program_ids = list()
        for program in self:
            if not program.rule_products_domain:
                valid_program_ids.append(program.id)
                continue
            valid_products = program._get_valid_products(products)
            if not valid_products:
                # The program can be directly discarded
                continue
            ordered_rule_products_qty = sum(products_qties[product] for product in valid_products)
            # Avoid program if 1 ordered foo on a program '1 foo, 1 free foo'
            """if program.promo_applicability == 'on_current_order' and \
               program.reward_type == 'product' and program._get_valid_products(program.reward_product_id):
                ordered_rule_products_qty -= program.reward_product_quantity"""
            if ordered_rule_products_qty >= program.rule_min_quantity:
                valid_program_ids.append(program.id)
        return self.browse(valid_program_ids)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_reward_values_discount(self, program):
        res = super(SaleOrder, self)._get_reward_values_discount(program)
        if program.discount_apply_on in ['specific_products', 'on_order']:
            return dict()
        return res

    def recompute_coupon_lines(self):
        for order in self:
            order._custom_remove_invalid_reward_lines()
            order._custom_create_new_no_code_promo_reward_lines()
            order._custom_update_existing_reward_lines()

    def _custom_remove_invalid_reward_lines(self):
        """ Find programs & coupons that are not applicable anymore.
            It will then unlink the related reward order lines.
            It will also unset the order's fields that are storing
            the applied coupons & programs.
            Note: It will also remove a reward line coming from an archive program.
        """
        self.ensure_one()
        order = self

        applied_programs = order._get_applied_programs()
        applicable_programs = self.env['coupon.program']
        if applied_programs:
            applicable_programs = order._get_applicable_programs() + order._get_valid_applied_coupon_program()
            applicable_programs = applicable_programs._keep_only_most_interesting_auto_applied_global_discount_program()
        programs_to_remove = applied_programs - applicable_programs

        reward_product_ids = applied_programs.discount_line_product_id.ids
        # delete reward line coming from an archived coupon (it will never be updated/removed when recomputing the order)
        invalid_lines = order.order_line.filtered(lambda line: line.is_reward_line and line.product_id.id not in reward_product_ids)

        if programs_to_remove:
            product_ids_to_remove = programs_to_remove.discount_line_product_id.ids

            if product_ids_to_remove:
                # Invalid generated coupon for which we are not eligible anymore ('expired' since it is specific to this SO and we may again met the requirements)
                self.generated_coupon_ids.filtered(lambda coupon: coupon.program_id.discount_line_product_id.id in product_ids_to_remove).write({'state': 'expired'})

            # Reset applied coupons for which we are not eligible anymore ('valid' so it can be use on another )
            coupons_to_remove = order.applied_coupon_ids.filtered(lambda coupon: coupon.program_id in programs_to_remove)
            coupons_to_remove.write({'state': 'new'})

            # Unbind promotion and coupon programs which requirements are not met anymore
            order.no_code_promo_program_ids -= programs_to_remove
            order.code_promo_program_id -= programs_to_remove

            if coupons_to_remove:
                order.applied_coupon_ids -= coupons_to_remove

            # Remove their reward lines
            #if product_ids_to_remove:
                #invalid_lines |= order.order_line.filtered(lambda line: line.product_id.id in product_ids_to_remove and line.is_reward_line)
        invalid_lines = order.order_line.filtered(lambda line: line.is_reward_line)
        if invalid_lines:
            self.env.cr.execute("DELETE FROM sale_order_line WHERE id IN (" + ",".join([str(id) for id in invalid_lines.ids]) +")")

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
            elif program.reward_type == 'product':
                self.write({'order_line': [(0, False, value) for value in self._get_custom_reward_line_values(program)]})
            order.no_code_promo_program_ids |= program

    def _get_applicable_no_code_promo_program(self):
        self.ensure_one()
        programs = self.env['coupon.program'].with_context(
            no_outdated_coupons=True,
            applicable_coupon=True,
        ).search([
            ('promo_code_usage', '=', 'no_code_needed'),
            '|', ('rule_date_from', '=', False), ('rule_date_from', '<=', self.date_order),
            '|', ('rule_date_to', '=', False), ('rule_date_to', '>=', self.date_order),
            '|', ('company_id', '=', self.company_id.id), ('company_id', '=', False),
        ])._filter_programs_from_common_rules(self)
        return programs

    def _get_custom_reward_line_values(self, program):
        self.ensure_one()
        self = self.with_context(lang=self.partner_id.lang)
        program = program.with_context(lang=self.partner_id.lang)
        if program.reward_type == 'product':
            return [self._get_custom_reward_values_product(program)]

    def _get_custom_reward_values_product(self, program):
        #price_unit = self.order_line.filtered(lambda line: program.reward_product_id == line.product_id)[0].price_reduce
        price_unit = 0.01

        order_lines = (self.order_line - self._get_reward_lines()).filtered(lambda x: program._get_valid_products(x.product_id))
        max_product_qty = sum(order_lines.mapped('product_uom_qty')) or 1
        total_qty = sum(self.order_line.filtered(lambda x: x.product_id == program.reward_product_id).mapped('product_uom_qty')) or 1
        # Remove needed quantity from reward quantity if same reward and rule product
        if program._get_valid_products(program.reward_product_id):
            # number of times the program should be appliedd
            #program_in_order = max_product_qty // (program.rule_min_quantity + program.reward_product_quantity)
            program_in_order = max_product_qty // (program.rule_min_quantity)
            # multipled by the reward qty
            reward_product_qty = program.reward_product_quantity * program_in_order
            # do not give more free reward than products
            reward_product_qty = min(reward_product_qty, total_qty)
            if program.rule_minimum_amount:
                order_total = sum(order_lines.mapped('price_total')) - (program.reward_product_quantity * program.reward_product_id.lst_price)
                reward_product_qty = min(reward_product_qty, order_total // program.rule_minimum_amount)
            reward_qty = reward_product_qty
        else:
            reward_qty = int(int(max_product_qty / program.rule_min_quantity) * program.reward_product_quantity)
            #reward_product_qty = min(max_product_qty, total_qty)


        #reward_qty = min(int(int(max_product_qty / program.rule_min_quantity) * program.reward_product_quantity), reward_product_qty)
        # Take the default taxes on the reward product, mapped with the fiscal position
        taxes = self.fiscal_position_id.map_tax(program.reward_product_id.taxes_id)
        return {
            'product_id': program.discount_line_product_id.id,
            'price_unit': price_unit,
            'product_uom_qty': reward_qty,
            'is_reward_line': True,
            'name': "(" + program.display_name +  ") " + "Free Product" + " - " + program.reward_product_id.name,
            'product_uom': program.reward_product_id.uom_id.id,
            'tax_id': [(4, tax.id, False) for tax in taxes]
        }

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
            values = order._get_custom_reward_line_values(program)
            lines = order.order_line.filtered(lambda line: line.product_id == program.discount_line_product_id)
            if not lines:
                return False
            if program.reward_type == 'discount' and program.discount_type == 'percentage':
                lines_to_remove = lines
                # Values is what discount lines should really be, lines is what we got in the SO at the moment
                # 1. If values & lines match, we should update the line (or delete it if no qty or price?)
                # 2. If the value is not in the lines, we should add it
                # 3. if the lines contains a tax not in value, we should remove it
                for value in values:
                    value_found = False
                    for line in lines:
                        # Case 1.
                        if not len(set(line.tax_id.mapped('id')).symmetric_difference(set([v[1] for v in value['tax_id']]))):
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
            #else:
            #    update_line(order, lines, values[0]).unlink()

    def _get_custom_reward_values_discount(self, program):
        order = self
        for line in order.order_line:
            if order._is_valid_product(program, line) and not line.is_reward_line:
                tmp_discount_sum = program.discount_percentage + line.discount_original
                if(line.is_discount_calculated and line.discount == tmp_discount_sum):
                    line.write({'discount_original': line.discount_original, 'discount_rate': line.discount_original})
                else:
                    line.write({'discount_original': line.discount, 'discount_rate': line.discount, 'is_discount_calculated': True})

                line.write({'discount_promotions': program.discount_percentage})
                discount_sum = line.discount_rate + line.discount_promotions

                line.write({'discount': discount_sum})

        return line

    def _is_valid_product(self, program, product):
        domain = ast.literal_eval(program.rule_products_domain) + [('id', '=', product.product_id.id)]
        return bool(self.env['product.product'].search_count(domain))