# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StatBookAddDataWizard(models.TransientModel):
    _name = 'stat.book.add.data.wizard'
    _description = 'Wizard per Aggiungere Dati Statistici'

    # Selezione divisione e dipartimento
    division_id = fields.Many2one(
        'stat.book.division',
        string='Divisione GDS',
        required=True
    )
    
    department_id = fields.Many2one(
        'stat.book.department',
        string='Dipartimento',
        required=True,
        domain="[('division_id', '=', division_id)]"
    )
    
    # Data e valore
    date = fields.Date(
        string='Data',
        required=True,
        default=fields.Date.context_today
    )
    
    value = fields.Float(
        string='Valore',
        required=True,
        default=0.0,
        help='Valore da aggiungere alle statistiche (es. totale pagamenti)'
    )
    
    # Note opzionali
    notes = fields.Text(string='Note')
    
    # Campi per il contesto del record chiamante
    res_model = fields.Char(string='Modello Origine')
    res_id = fields.Integer(string='ID Origine')
    
    # Campo per mostrare l'anteprima della selezione
    preview_text = fields.Char(
        string='Anteprima',
        compute='_compute_preview_text',
        readonly=True
    )
    
    @api.depends('division_id', 'department_id')
    def _compute_preview_text(self):
        for wizard in self:
            if wizard.division_id and wizard.department_id:
                wizard.preview_text = f"{wizard.division_id.name} - {wizard.department_id.name}"
            elif wizard.division_id:
                wizard.preview_text = wizard.division_id.name
            else:
                wizard.preview_text = "Seleziona divisione e dipartimento"
    
    @api.onchange('division_id')
    def _onchange_division_id(self):
        """Reset department quando cambia la divisione"""
        self.department_id = False
        if self.division_id:
            # Se la divisione ha un solo dipartimento, selezionalo automaticamente
            departments = self.env['stat.book.department'].search([
                ('division_id', '=', self.division_id.id),
                ('active', '=', True)
            ])
            if len(departments) == 1:
                self.department_id = departments[0]
    
    def action_add_data(self):
        """Aggiunge i dati statistici e chiude il wizard"""
        self.ensure_one()
        
        if self.value == 0:
            raise ValidationError("Il valore non può essere zero")
        
        # Crea il record dei dati statistici
        self.env['stat.book.data'].create({
            'department_id': self.department_id.id,
            'date': self.date,
            'value': self.value,
            'res_model': self.res_model,
            'res_id': self.res_id,
            'notes': self.notes,
        })
        
        return {'type': 'ir.actions.act_window_close'}
    
    @api.model
    def open_wizard_from_record(self, res_model, res_id, value=0.0, date=None):
        """
        Metodo helper per aprire il wizard da altri moduli
        
        Args:
            res_model: Nome del modello chiamante
            res_id: ID del record chiamante
            value: Valore predefinito da inserire
            date: Data predefinita (se None, usa oggi)
        
        Returns:
            Action per aprire il wizard
        """
        if date is None:
            date = fields.Date.context_today(self)
        
        wizard = self.create({
            'res_model': res_model,
            'res_id': res_id,
            'value': value,
            'date': date,
        })
        
        return {
            'name': 'Aggiungi a Stat Book',
            'type': 'ir.actions.act_window',
            'res_model': 'stat.book.add.data.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
