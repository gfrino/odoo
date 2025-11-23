# -*- coding: utf-8 -*-
{
    'name': 'TW Stat Book - Account Integration Example',
    'version': '1.0',
    'category': 'Statistics',
    'summary': 'Esempio di integrazione Stat Book con modulo Account',
    'description': """
        Questo è un modulo di esempio che mostra come integrare 
        TW Stat Book con il modulo contabilità di Odoo.
        
        NOTA: Questo è solo un esempio di riferimento.
        Non installare questo modulo in produzione.
    """,
    'author': 'TW',
    'depends': ['tw_stat_book', 'account'],
    'data': [
        'views/account_payment_inherit_views.xml',
    ],
    'installable': False,  # Disabilitato di default, è solo un esempio
    'auto_install': False,
    'license': 'LGPL-3',
}
