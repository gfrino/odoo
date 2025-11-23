# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'
    
    def action_open_stat_book_wizard(self):
        """
        Apre il wizard per aggiungere questo pagamento alle statistiche
        """
        self.ensure_one()
        
        # Calcola il valore da aggiungere (in questo caso l'importo del pagamento)
        value = self.amount
        
        # Apri il wizard
        return self.env['stat.book.add.data.wizard'].open_wizard_from_record(
            res_model=self._name,
            res_id=self.id,
            value=value,
            date=self.date or fields.Date.context_today(self)
        )
