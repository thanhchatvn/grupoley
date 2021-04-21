# -*- coding: utf-8 -*-
{
    'name': "Partner CFDI",

    'summary': """
        Módulo que agrega el uso de CFDI en el catalogo de contactos
    """,

    'description': """
        Módulo que agrega el uso de CFDI en el catalogo de contactos para poder asignarlo individualmente
        desde la alta de un contacto y que se vea reflejado en la facturación
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contacts',
    'version': '14.0.1',

    'depends': ['base','account','l10n_mx_edi'],

    'data': [
        'views/res_partner.xml',
    ],
    'demo': [
    ],
}
