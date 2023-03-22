# -*- coding: utf-8 -*-

{
    'name': 'Modulo MICRO',
    'version': '1.0',
    'depends': [
        'contacts',
    ],
    'author': 'Angel Guevara',
    'category': 'ERP',
    'website': 'www.google.com',
    'summary': 'Modulo para administracion de local',
    'description': '''
    Modulo para administracion de locales
    ''',
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'data/categoria.xml',
        'data/micro_secuencia.xml',
        # 'wizard/update_wizard_views.xml',
        'views/micro_ticket_view.xml',
        'views/menu.xml',
    ],
}