# -*- coding: utf-8 -*-
{
    'name': "additional_discount_promotion",

    'summary': """
        Módulo que nos permite agregar un descuento en casacada en las promociones.
     """,

    'description': """
        Módulo que modifica el desarrollo de custom_promotions añadiendo un descuento extra llamado descuento en cascada.
    """,

    'author': "Soporte Grupo Ley",
    
    'website': "todoo.grupoley.com",
   
    'category': 'Sale',
    
    'version': '14.0.1',

    'depends': ['base', 'sale','coupon', 'sale_coupon','custom_promotions'],

    'data': [
        'views/inherit_coupon_program.xml',
    ],
    
    'demo': [
    ],
}
