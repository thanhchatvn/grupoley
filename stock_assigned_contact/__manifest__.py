# -*- coding: utf-8 -*-
{
    'name': "contact",

    'summary': """
        Contact/View of the Recepciones""",

    'description': """
        Modúlo creado para visualizar en pantalla de Entrada por compra el nombre del contacto
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
