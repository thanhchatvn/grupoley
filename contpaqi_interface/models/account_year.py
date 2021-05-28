# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountYear(models.Model):
    _name = 'account.year'
    _description = 'Ejercicio contable'

    name = fields.Char(string='Ejercicio')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)

    @api.model
    def get_account_year(self):
        account_year_obj = self.env['account.year'].search([('company_id','=',self.env.company.id)])
        account_year_obj.unlink()
        connection = self.env['contpaqi.interface'].server_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("Select Distinct ejercicio as Nombre From nom10002(Nolock)")
                batchs = cursor.fetchall()
                for batch in batchs:
                    data = {
                        'name': batch[0]
                    }
                    account_year_obj.create(data)
        except Exception as e:
            print('No es posible realizar la consulta', e)
