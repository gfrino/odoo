# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StatBookDepartment(models.Model):
    _name = 'stat.book.department'
    _description = 'Dipartimento'
    _order = 'division_id, sequence, name'

    name = fields.Char(string='Nome Dipartimento', required=True)
    sequence = fields.Integer(string='Sequenza', default=10)
    
    # Relazione con la divisione
    division_id = fields.Many2one(
        'stat.book.division', 
        string='Divisione', 
        required=True,
        ondelete='cascade'
    )
    
    # Previsioni per il dipartimento
    forecast_min_3months = fields.Float(
        string='Previsione Minima (3 mesi)', 
        default=0.0,
        help='Valore minimo previsto per i grafici nei prossimi 3 mesi'
    )
    forecast_max_3months = fields.Float(
        string='Previsione Massima (3 mesi)', 
        default=100.0,
        help='Valore massimo previsto per i grafici nei prossimi 3 mesi'
    )
    
    # Relazione con i dati statistici
    data_ids = fields.One2many(
        'stat.book.data', 
        'department_id', 
        string='Dati Statistici'
    )
    
    active = fields.Boolean(string='Attivo', default=True)
    
    # Campo computato per il nome completo
    display_name_full = fields.Char(
        string='Nome Completo', 
        compute='_compute_display_name_full',
        store=True
    )
    
    @api.depends('name', 'division_id.name')
    def _compute_display_name_full(self):
        for record in self:
            if record.division_id:
                record.display_name_full = f"{record.division_id.name} - {record.name}"
            else:
                record.display_name_full = record.name
    
    @api.constrains('forecast_min_3months', 'forecast_max_3months')
    def _check_forecast_values(self):
        for record in self:
            if record.forecast_min_3months > record.forecast_max_3months:
                raise models.ValidationError(
                    'La previsione minima non può essere maggiore della previsione massima'
                )
