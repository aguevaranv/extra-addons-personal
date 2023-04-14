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
        'views/menu.xml',
        'data/micro_secuencia.xml',
        'wizard/micro_update_abono_wizard_views.xml',
        'views/micro_ticket_por_retirar_view.xml',
        'views/micro_ticket_entregado_view.xml',
        'views/micro_ticket_view.xml',
        'views/micro_movimiento_view.xml',
    ],
}