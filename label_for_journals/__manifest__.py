# -*- coding: utf-8 -*-
{
    'name': "Label for journals",

    'summary': """
        Este módulo nos permite visualizar la etiqueta de diario en una factura.
    """,

    'description': """
        Este módulo nos permite visualizar la etiqueta de diario en una factura, ya que este label solo era visible
        para el grupo de Facturación/Auditor.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",


    'category': 'Account',

    'version': '14.0.1',

    'depends': ['base','account', 'account_accountant'],

    'data': [
        'views/account_move.xml',
    ],
    'demo': [
    ],
}
