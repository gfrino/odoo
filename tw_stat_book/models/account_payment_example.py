# -*- coding: utf-8 -*-
# Esempio di integrazione del modulo Stat Book con il modulo account (contabilità)

from odoo import models, fields, api


class AccountPaymentInherit(models.Model):
    """
    Esempio di come estendere il modulo account.payment per integrare Stat Book
    Questo è solo un esempio - andrà adattato al tuo modulo specifico
    """
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


# Per aggiungere il pulsante nella vista form di account.payment,
# crea un file XML views/account_payment_inherit_views.xml con:
#
# <?xml version="1.0" encoding="utf-8"?>
# <odoo>
#     <record id="view_account_payment_form_inherit_stat_book" model="ir.ui.view">
#         <field name="name">account.payment.form.inherit.stat.book</field>
#         <field name="model">account.payment</field>
#         <field name="inherit_id" ref="account.view_account_payment_form"/>
#         <field name="arch" type="xml">
#             <xpath expr="//header" position="inside">
#                 <button name="action_open_stat_book_wizard" 
#                         type="object" 
#                         string="Stat Book"
#                         icon="fa-line-chart"
#                         groups="tw_stat_book.group_stat_book_admin"
#                         class="oe_highlight"/>
#             </xpath>
#         </field>
#     </record>
# </odoo>
