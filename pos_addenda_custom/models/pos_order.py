# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    inputValue1 = fields.Char(string='inputValue1')
    inputValue2 = fields.Char(string='inputValue2')
    inputValue3 = fields.Char(string='inputValue3')
    inputValue4 = fields.Char(string='inputValue4')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['inputValue1'] = ui_order.get('inputValue1', False)
        res['inputValue2'] = ui_order.get('inputValue2', False)
        res['inputValue3'] = ui_order.get('inputValue3', False)
        res['inputValue4'] = ui_order.get('inputValue4', False)
        return res

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        if self.inputValue1 and self.inputValue2 and self.inputValue3 and self.inputValue4:
            res['x_order_reference'] = self.inputValue1
            res['x_order_reference_date'] = self.inputValue2
            res['x_delivery_reference'] = self.inputValue3
            res['x_delivery_reference_date'] = self.inputValue4
        partner_id = self.env['res.partner'].browse(res['partner_id'])
        if partner_id.property_payment_term_id:
            res['invoice_payment_term_id'] = partner_id.property_payment_term_id.id
        return res

    def buscar_addenda_parent(self, partner):
        if self.env['res.partner'].browse(partner).l10n_mx_edi_addenda:
            return True
        return False
