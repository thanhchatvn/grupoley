# -*- coding: utf-8 -*-
{
    'name': "Consume all from production orders",

    'summary': """
        Módulo que nos ayuda a consumir todos los insumos de una orden de produccion
    """,

    'description': """
        Módulo que nos permite el consumir todos los insumos que 
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com",

    'category': 'Mrp',

    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        'views/mrp_production.xml',
    ],

    'demo': [
    ],
}
