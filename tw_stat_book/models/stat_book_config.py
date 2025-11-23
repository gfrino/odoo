# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StatBookConfig(models.Model):
    _name = 'stat.book.config'
    _description = 'Configurazione Stat Book'
    _rec_name = 'id'

    week_start_day = fields.Selection([
        ('0', 'Lunedì'),
        ('1', 'Martedì'),
        ('2', 'Mercoledì'),
        ('3', 'Giovedì'),
        ('4', 'Venerdì'),
        ('5', 'Sabato'),
        ('6', 'Domenica'),
    ], string='Inizio Settimana', default='3', required=True,
        help='Seleziona il giorno di inizio della settimana per i grafici settimanali')

    @api.model
    def get_week_start_day(self):
        """Restituisce il giorno di inizio settimana configurato"""
        config = self.search([], limit=1)
        if not config:
            config = self.create({'week_start_day': '3'})
        return int(config.week_start_day)
