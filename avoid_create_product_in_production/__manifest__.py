# -*- coding: utf-8 -*-
{
    'name': "Avoid create product in production plan",

    'summary': """
        Este modelo deshabilita la creación de productos desde el plan maestro de producción
    """,

    'description': """
        Este modelo deshabilita la creación de productos desde el plan maestro de producción
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com",

    'category': 'Mrp',

    'version': '14.0.1',

    'depends': ['base','mrp','mrp_mps'],

    'data': [
        'views/production_schedule.xml',
    ],

    'demo': [
    ],
}
