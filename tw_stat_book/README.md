# TW Stat Book

## Descrizione

Modulo Odoo per la gestione di grafici statistici organizzati per divisioni e dipartimenti GDS.

## Caratteristiche Principali

### Gestione Divisioni e Dipartimenti
- **6 Divisioni GDS** configurabili
- **3 Dipartimenti** per ogni divisione
- Previsioni minime e massime personalizzabili per ogni livello

### Visualizzazione Grafici
- Grafici a linee interattivi
- Tre modalità di visualizzazione:
  - **Settimanale**: dati aggregati per settimana
  - **Mensile**: dati aggregati per mese
  - **Annuale**: dati aggregati per anno
- Limiti del grafico basati sulle previsioni configurate

### Integrazione con Altri Moduli
- Pulsante widget per aggiungere dati da qualsiasi vista Odoo
- Wizard intuitivo per la selezione di divisione/dipartimento
- Tracciamento automatico dell'origine dei dati

### Permessi di Sicurezza
- **Utente**: visualizzazione grafici e dati
- **Amministratore**: configurazione completa e aggiunta dati

## Installazione

1. Copiare il modulo nella directory `extra-addons-tw`
2. Aggiornare la lista dei moduli in Odoo
3. Installare il modulo "TW Stat Book"

## Configurazione Iniziale

1. Andare su **Stat Book > Configurazione > Impostazioni**
2. Configurare il giorno di inizio della settimana (default: Giovedì)
3. Creare le 6 divisioni GDS in **Configurazione > Divisioni GDS**
4. Per ogni divisione, aggiungere 3 dipartimenti con le relative previsioni

### Esempio di Configurazione

```
GDS Divisione 1
  - Previsione minima: 5
  - Previsione massima: 10
  - Dipartimenti:
    * Dipartimento 1 (min: 2, max: 5)
    * Dipartimento 2 (min: 1, max: 3)
    * Dipartimento 3 (min: 2, max: 2)
```

## Utilizzo

### Aggiungere Dati Statistici

Per integrare Stat Book in altri moduli, aggiungere il widget nella vista form:

```xml
<button name="%(tw_stat_book.action_stat_book_add_data_wizard)d" 
        type="action" 
        string="Stat Book"
        icon="fa-line-chart"
        groups="tw_stat_book.group_stat_book_admin"/>
```

### Visualizzare i Grafici

1. Andare su **Stat Book > Grafici > Visualizza Grafici**
2. Selezionare il dipartimento desiderato
3. Scegliere la modalità di visualizzazione (Settimanale/Mensile/Annuale)

## API per Sviluppatori

### Aggiungere Dati Programmaticamente

```python
# Metodo 1: Diretto
self.env['stat.book.data'].add_stat_data(
    department_id=dept_id,
    value=100.0,
    date='2025-11-23',
    res_model='sale.order',
    res_id=order_id
)

# Metodo 2: Tramite Wizard
wizard_action = self.env['stat.book.add.data.wizard'].open_wizard_from_record(
    res_model='account.payment',
    res_id=payment_id,
    value=payment.amount
)
return wizard_action
```

### Ottenere Dati per Grafici

```python
chart_data = self.env['stat.book.data'].get_chart_data(
    department_id=dept_id,
    view_type='monthly',  # 'weekly', 'monthly', 'yearly'
    date_from='2025-01-01',
    date_to='2025-12-31'
)
```

## Struttura del Modulo

```
tw_stat_book/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── stat_book_config.py
│   ├── stat_book_division.py
│   ├── stat_book_department.py
│   └── stat_book_data.py
├── views/
│   ├── stat_book_division_views.xml
│   ├── stat_book_department_views.xml
│   ├── stat_book_data_views.xml
│   ├── stat_book_config_views.xml
│   ├── stat_book_chart_views.xml
│   └── stat_book_menu_views.xml
├── wizard/
│   ├── __init__.py
│   ├── stat_book_add_data_wizard.py
│   └── stat_book_add_data_wizard_views.xml
├── security/
│   ├── stat_book_security.xml
│   └── ir.model.access.csv
└── static/
    ├── src/
    │   ├── js/
    │   │   ├── stat_book_chart_widget.js
    │   │   └── stat_book_button_widget.js
    │   ├── xml/
    │   │   └── stat_book_templates.xml
    │   └── css/
    │       └── stat_book.css
    └── description/
        └── icon.png
```

## Note Importanti

- I grafici mostrano solo i valori entro i limiti delle previsioni configurate
- Se un valore supera il massimo previsto, la linea continuerà ma il valore non sarà visibile
- È necessario aggiornare le previsioni per visualizzare valori fuori range
- Il grafico utilizza Chart.js (assicurarsi che sia disponibile in Odoo)

## Supporto

Per problemi o richieste di funzionalità, contattare il team TW.

## Licenza

LGPL-3
