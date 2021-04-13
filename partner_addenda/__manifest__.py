# -*- coding: utf-8 -*-
{
    'name': "Partner Addenda",

    'summary': """
        Agregar todas las addendas que se vayan desarrollando
    """,

    'description': """
        Este módulo permite agregar y modificar las addendas
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Uncategorized',

    'version': '14.0.1',

    'depends': ['base','l10n_mx_edi','contacts'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/addenda_chedrahui.xml',
        'views/addenda_farmacias_guadalajara.xml',
        'views/addenda_casa_ley.xml',
    ],

    'demo': [
    ],
}
