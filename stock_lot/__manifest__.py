# -*- coding: utf-8 -*-
{
    'name': "stock_lot",

    'summary': """
        Stock Lot/Serial""",

    'description': """
        Este modulo tiene como función saber cuales lotes hay en existencia en ubicacion seleccionada
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
