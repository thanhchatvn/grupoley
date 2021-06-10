# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero, float_round
from odoo.exceptions import ValidationError, UserError
from odoo.http import request
from odoo.osv.expression import AND
import base64


class PosOrder(models.Model):
    _inherit = "pos.order"

    def action_pos_order_invoice(self):
            moves = self.env['account.move']

            for order in self:
                # Force company for all SUPERUSER_ID action
                if order.account_move:
                    moves += order.account_move
                    continue

                if not order.partner_id:
                    raise UserError(_('Please provide a partner for the sale.'))

                move_vals = order._prepare_invoice_vals()
                new_move = order._create_invoice(move_vals)
                order.write({'account_move': new_move.id, 'state': 'invoiced'})
                new_move.sudo().with_company(order.company_id)._post()
                print('pos order post')
                new_move.sudo().with_company(order.company_id).action_process_edi_web_services()
                moves += new_move

            if not moves:
                return {}

            return {
                'name': _('Customer Invoice'),
                'view_mode': 'form',
                'view_id': self.env.ref('account.view_move_form').id,
                'res_model': 'account.move',
                'context': "{'move_type':'out_invoice'}",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': moves and moves.ids[0] or False,
            }

