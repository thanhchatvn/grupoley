# -*- coding: utf-8 -*-
{
    'name': "CONTPAQi Nomina",

    'summary': """
        Interfaz de software CONTPAQi nominas hacia Odoo
    """,

    'description': """
        Modulo que nos permite interfazar CONTPAQi y Odoo para afectar la contabilidad por medio de
        las polizas generadas en CONTPAQi afectando asientos contables en Odoo.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Interfaz',

    'version': '14.0.1',

    'depends': ['base','account','sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_company.xml',
        'views/period_type.xml',
        'views/account_year.xml',
        'views/period_number.xml',
        'views/account_move_line.xml',
        'views/temporal.xml',
        'views/temp.xml',
        'views/payroll_rule.xml',
        'views/accounting_policy.xml',
        'security/contpaqi_security_rules.xml',
    ],

    'demo': [
    ],
}
