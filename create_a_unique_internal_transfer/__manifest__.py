# -*- coding: utf-8 -*-
{
    'name': "Create a unique internal transfer",

    'summary': """
        Sobreescritura del metodo assign_picking para crear trasnferencias internas diferentes
    """,

    'description': """
        Creación de diferentes ordens de transferencia para evitar que se acumulen en una sola orden y
        poder llevar un mejor control.
    """,

    'author': "Soporte Grupo ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Stock',

    'version': '14.0.1',

    'depends': ['base','stock','mrp'],

    'data': [
    ],
    'demo': [
    ],
}
