# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PeriodNumbers(models.Model):
    _name = 'period.number'
    _description = 'Numero de periodos'

    code = fields.Char(string='Código')
    name = fields.Char(string='Numero de Periodo')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)



    def _get_period_number(self,period_type):
        try:
            period_number_obj = self.env['period.number'].search([('company_id', '=', self.env.company.id)])
            period_number_obj.unlink()
            connection = self.env['contpaqi.interface'].server_connection()

            with connection.cursor() as cursor:
                cursor.execute("""
                                Select distinct q.idtipoperiodo as Codigo,p.numeroperiodo as Nombre
                                from nom10023 q (nolock)
                                inner join nom10002 p (nolock) on q.idtipoperiodo=p.idtipoperiodo
                                inner join nom10007 l (nolock) on l.idperiodo=p.idperiodo
                                where q.idtipoperiodo=""" + str(period_type.code))
                batchs = cursor.fetchall()
                for batch in batchs:
                    data = {
                        'code': batch[0],
                        'name': batch[1]
                    }
                    period_number_obj.create(data)
            return period_type
        except Exception as e:
            return period_type
            print('No es posible realizar la consulta initial methods', e)
        finally:
            connection.close()
