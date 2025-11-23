# -*- coding: utf-8 -*-
{
    'name': 'TW Stat Book',
    'version': '1.0',
    'category': 'Statistics',
    'summary': 'Gestione grafici statistici con previsioni e dati effettivi',
    'description': """
        Modulo per la gestione di grafici statistici organizzati per divisioni e dipartimenti.
        
        Caratteristiche principali:
        - Gestione di 6 divisioni GDS con 3 dipartimenti ciascuna
        - Previsioni minime e massime personalizzabili per ogni divisione/dipartimento
        - Visualizzazione grafici a linee con viste Mensile, Settimanale e Annuale
        - Integrazione con altri moduli tramite widget pulsante grafico
        - Permessi Utente (visualizzazione) e Amministratore (configurazione)
    """,
    'author': 'TW',
    'website': '',
    'depends': ['base', 'web'],
    'data': [
        'security/stat_book_security.xml',
        'security/ir.model.access.csv',
        'views/stat_book_division_views.xml',
        'views/stat_book_department_views.xml',
        'views/stat_book_data_views.xml',
        'views/stat_book_config_views.xml',
        'views/stat_book_chart_views.xml',
        'views/stat_book_menu_views.xml',
        'wizard/stat_book_add_data_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tw_stat_book/static/src/js/stat_book_chart_widget.js',
            'tw_stat_book/static/src/js/stat_book_button_widget.js',
            'tw_stat_book/static/src/xml/stat_book_templates.xml',
            'tw_stat_book/static/src/css/stat_book.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
