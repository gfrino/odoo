# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,date


class VsdSettings(models.Model):
    _name = 'vsd.setting'
    _description = 'VSD Setting Page'
    _rec_name = 'vsd_type'
    
    
    @api.model
    def create(self, vals):
        exists = self.search([('user_id','=',vals['user_id'])])
        
        if exists:
            raise UserError(('Current user is already exists in VSD Setting!'))
        else:
            pass
           
        rec = super(VsdSettings, self).create(vals)
        return rec
    
    
    vsd_type = fields.Selection([('based_on_invoice','Based on Invoice')], string='Type', required=True, default='based_on_invoice')
    servizio =  fields.Selection([('Facebook Marketing','Social Media Marketing'), ('Google Ads','Google Ads'),
                                  ('Email Marketing','Email Marketing'), ('Website','Website'),
                                  ('eCommerce','eCommerce'), ('Odoo','Odoo'), ('Video', 'Video'),
                                  ('Pacchetto Assistenza','Pacchetto Assistenza'),('Grafica','Grafica')], string="Servizio")
    
    category_id = fields.Many2one('product.category', string="Applied on Category")
    user_id = fields.Many2one('res.users', string='Assign To')
    vsd_points = fields.Float(string='VSD Points')
    

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            vsd_value_amount = float(self.env['ir.config_parameter'].sudo().get_param('vsd_value_amount')),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('vsd_value_amount', self.vsd_value_amount)



    
    vsd_value_amount = fields.Float(string='VSD Value Amount')
    
        
    
    
    