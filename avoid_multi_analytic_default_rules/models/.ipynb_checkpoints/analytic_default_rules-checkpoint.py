# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class avoid_multi_analytic_default_rules(models.Model):
    _inherit = 'account.analytic.default'

    @api.constrains('product_id', 'user_id', 'company_id', 'account_id')
    def _check_analytic_rules(self):
        analytic_rules_obj = self.env['account.analytic.default'].search([
            '&', '&', '&',
            ('product_id', '=', self.product_id.id),
            ('user_id', '=', self.user_id.id),
            ('company_id', '=', self.company_id.id),
            ('account_id', '=', self.account_id.id)
        ],limit=2)

        if len(analytic_rules_obj) > 1:
            raise UserError(_("La regla analítica ya existe, si desea modificarla su id es [%s]" % analytic_rules_obj[0].id))
