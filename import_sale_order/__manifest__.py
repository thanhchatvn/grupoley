# -*- coding: utf-8 -*-
{
    'name': "Import Sale Order",

    'summary': """
        Módulo que realiza la importación de datos desde un pedido de compra agrupado en un archivo de texto     
    """,

    'description': """
        Módulo que realiza la importación de datos desde un pedido de compra agrupado en un archivo de texto
        que proporciona Casa Ley a sus proveedores con la finalidad de facilitar los procedimientos
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Sales',

    'version': '14.0.1',

    'depends': ['base','sale_management','partner_addenda','stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/import_sale_order.xml',
    ],

    'demo': [
    ],
}
