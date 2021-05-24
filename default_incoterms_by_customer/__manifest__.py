# -*- coding: utf-8 -*-
{
    'name': "Default Incoterms By Costumers",
    'summary': """
        Nos permite colocar por default los tratos de comercio internacional por cliente
    """,
    'description': """
        Nos permite colocar por default los tratos de comercio internacional por cliente agregando un nuevo campo
        en el catalogo de clientes
    """,
    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'Contacts',
    'version': '14.0.1',
    'depends': ['base','contacts','account','sale_management'],
    'data': [
        'views/res_partner.xml',
    ],
    'demo': [
    ],
}