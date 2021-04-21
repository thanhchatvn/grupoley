# -*- coding: utf-8 -*-
{
    'name': "Exchange rate amount",

    'summary': """
        Módulo para obtener el monto de la tasa de cambio en 4 digitos""",

    'description': """
        Este módulo nos ayuda a modificar la vista de 'res.currency.rate' para agregar la tasa de cambio
        con 4 digitos y tener una mejor visibilidad del cambio
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Uncategorized',

    'version': '14.0.1',

    'depends': ['base','account'],

    'data': [
        'views/res_currency_rate.xml',
    ],

    'demo': [
    ],
}
