# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StatBookData(models.Model):
    _name = 'stat.book.data'
    _description = 'Dati Statistici'
    _order = 'date desc, id desc'

    name = fields.Char(string='Descrizione', compute='_compute_name', store=True)
    
    # Relazione con il dipartimento
    department_id = fields.Many2one(
        'stat.book.department', 
        string='Dipartimento', 
        required=True,
        ondelete='cascade'
    )
    
    division_id = fields.Many2one(
        'stat.book.division',
        string='Divisione',
        related='department_id.division_id',
        store=True,
        readonly=True
    )
    
    # Data del dato statistico
    date = fields.Date(
        string='Data', 
        required=True,
        default=fields.Date.context_today,
        index=True
    )
    
    # Valore statistico
    value = fields.Float(
        string='Valore', 
        required=True,
        default=0.0,
        help='Valore totale per questa data (es. somma dei pagamenti)'
    )
    
    # Riferimento generico al record sorgente (opzionale)
    res_model = fields.Char(
        string='Modello Riferimento',
        help='Modello Odoo da cui proviene questo dato (es. account.payment)'
    )
    
    res_id = fields.Integer(
        string='ID Riferimento',
        help='ID del record nel modello di riferimento'
    )
    
    # Note aggiuntive
    notes = fields.Text(string='Note')
    
    # Utente che ha inserito il dato
    user_id = fields.Many2one(
        'res.users',
        string='Inserito da',
        default=lambda self: self.env.user,
        readonly=True
    )
    
    create_date = fields.Datetime(string='Data Creazione', readonly=True)
    
    @api.depends('department_id', 'date', 'value')
    def _compute_name(self):
        for record in self:
            if record.department_id and record.date:
                record.name = f"{record.department_id.display_name_full} - {record.date} - {record.value}"
            else:
                record.name = 'Nuovo Dato Statistico'
    
    @api.model
    def add_stat_data(self, department_id, value, date=None, res_model=None, res_id=None, notes=None):
        """
        Metodo helper per aggiungere dati statistici da altri moduli
        """
        if date is None:
            date = fields.Date.context_today(self)
        
        vals = {
            'department_id': department_id,
            'value': value,
            'date': date,
            'res_model': res_model,
            'res_id': res_id,
            'notes': notes,
        }
        
        return self.create(vals)
    
    @api.model
    def get_chart_data(self, department_id, view_type='monthly', date_from=None, date_to=None):
        """
        Restituisce i dati aggregati per i grafici
        view_type: 'weekly', 'monthly', 'yearly'
        """
        domain = [('department_id', '=', department_id)]
        
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        
        data = self.search(domain)
        
        # Aggregazione dei dati per periodo
        aggregated = {}
        
        for record in data:
            if view_type == 'weekly':
                # Raggruppa per settimana
                week_key = record.date.isocalendar()[:2]  # (anno, settimana)
                key = f"{week_key[0]}-W{week_key[1]:02d}"
            elif view_type == 'monthly':
                # Raggruppa per mese
                key = record.date.strftime('%Y-%m')
            elif view_type == 'yearly':
                # Raggruppa per anno
                key = str(record.date.year)
            else:
                # Default: giornaliero
                key = record.date.isoformat()
            
            if key not in aggregated:
                aggregated[key] = 0.0
            
            aggregated[key] += record.value
        
        # Converti in lista ordinata
        result = [{'period': k, 'value': v} for k, v in sorted(aggregated.items())]
        
        return result
