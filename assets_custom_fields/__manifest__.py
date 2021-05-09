# -*- coding: utf-8 -*-
{
    'name': "Asset Custom Fields",

    'summary': """
        Modelo para agregar en el catalogo de activos el INCP y el departamento
    """,

    'description': """
        Modelo para agregar en el catalogo de activos el INCP y el departamento para completar los datos requeridos.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Accounting',

    'version': '14.0.1',

    'depends': ['base','account_asset'],

    'data': [
        'views/account_assets.xml',
    ],
    'demo': [
    ],
}
