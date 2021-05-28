# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PeriodType(models.Model):
    _name = 'period.type'
    _description = 'Tipo de periodos'

    code = fields.Char(string='Código')
    name = fields.Char(string='Tipo de Periodo')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)
    counter = fields.Integer(string='Contador', store=True)

    @api.model
    def get_period_type(self):
        try:
            period_type_obj = self.env['period.type'].search([('company_id', '=', self.env.company.id)])
            period_type_obj.unlink()
            connection = self.env['contpaqi.interface'].server_connection()
            with connection.cursor() as cursor:
                cursor.execute("Select IdtipoPeriodo as Codigo,NombretipoPeriodo as Nombre From nom10023(Nolock)")
                batchs = cursor.fetchall()
                for batch in batchs:
                    data = {
                        'code': batch[0],
                        'name': batch[1]
                    }
                    period_type_obj.create(data)
        except Exception as e:
            print('No es posible realizar la consulta', e)
