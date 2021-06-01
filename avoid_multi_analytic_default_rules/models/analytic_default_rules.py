# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class avoid_multi_analytic_default_rules(models.Model):
    _inherit = 'account.analytic.default'
    
    company_id = fields.Many2one('res.company', string='Company', default= lambda self: self.env.company, ondelete='cascade', help="Select a company which will use analytic account specified in analytic default (e.g. create new customer invoice or Sales order if we select this company, it will automatically take this as an analytic account)")


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
