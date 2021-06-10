# -*- coding: utf-8 -*-
{
    'name': "POS request automatic addenda",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
         'l10n_mx_edi',
         'partner_addenda',
         'res_partner_cfdi',
    ],
    'author': "DataWorks",
    'category': 'Sale',
    'description': "Permite llamar a accion que genera timbrado al validar order en POS",
    'summary': "Permite llamar a acccion que genera timbrado al validar order en POS",

    'data': [
        # 'views/templates.xml',
    ],

    'qweb': [
    ],
}
