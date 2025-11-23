# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StatBookDivision(models.Model):
    _name = 'stat.book.division'
    _description = 'Divisione GDS'
    _order = 'sequence, name'

    name = fields.Char(string='Nome Divisione', required=True)
    sequence = fields.Integer(string='Sequenza', default=10)
    
    # Previsioni per la divisione
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
    
    # Relazione con i dipartimenti
    department_ids = fields.One2many(
        'stat.book.department', 
        'division_id', 
        string='Dipartimenti'
    )
    
    active = fields.Boolean(string='Attivo', default=True)
    
    @api.constrains('forecast_min_3months', 'forecast_max_3months')
    def _check_forecast_values(self):
        for record in self:
            if record.forecast_min_3months > record.forecast_max_3months:
                raise models.ValidationError(
                    'La previsione minima non può essere maggiore della previsione massima'
                )
