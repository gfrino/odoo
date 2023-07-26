# coding: utf-8

import datetime
from datetime import date
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
import base64


class AccountPaymentVsd(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment VSD'


    def post(self):
        agent_obj = None
        inv_no = None
        
        res = super(AccountPaymentVsd, self).post()
        for inv in self.invoice_ids:
            inv_no = inv.name
        
        if inv_no: 
            category_ids = False  
            generate_entry = False 
            user_id = False
            
            move_record = self.env['account.move'].search([('name','=',inv_no),('type','=','out_invoice')])
            
            if move_record:
                if move_record.invoice_line_ids:
                    for line in move_record.invoice_line_ids:
                        cat_id = line.product_id.categ_id.id
                        
                        #search category in vsd setting menu
                        setting_rec = self.env['vsd.setting'].search([('vsd_type','=','based_on_invoice'),('category_id','=',cat_id)], order="id desc", limit=1)
                        
                        if setting_rec:
                            generate_entry = True
                            break

                    
            if generate_entry:
                """Creating entry to VSD"""
                vsd_value = 0
                category_id = setting_rec.category_id
                user_id = setting_rec.user_id
                vsd_points = setting_rec.vsd_points
                
                if move_record:
                    for line in move_record.invoice_line_ids:
                        if line.product_id.categ_id.id == category_id.id:
                            vsd_value = line.price_subtotal
                    
                if user_id: 
                    employee_rec = self.env['hr.employee'].search([('user_id', '=', user_id.id)], order='id desc', limit=1)
                    employee = employee_rec.id
                else:
                    employee = None
                    
                entry_exists = self.env['vsd.point.entry.line'].search([('move_id', '=', move_record.id)])
 
                if not entry_exists:
                    vals = {
                        'move_id': move_record.id,
                        'points_value': vsd_points,
                        'vsd_value': vsd_value,
                        'customer_id': move_record.partner_id.id,
                        'employee_id': employee,
                        'date': fields.Date.today(),
                        'servizio': 'Hosting',
                    }
                    record = self.env['vsd.point.entry.line'].create(vals)
                    record.update({'servizio':'Hosting'})
                    print('record----servizio--',record.servizio)
                    found = False
                    vsd_rec = self.env['vsd.point.entry'].search([('state', '=', 'open')])
                  
                    if vsd_rec:
                        record.line_id = vsd_rec.id
                    else:
                        vals = {
                            'date_from':fields.Date.today(),
                        }
                        p_record = self.env['vsd.point.entry'].create(vals)
                        record.line_id = p_record.id
                         
                else:
                    vals = {
                        'points_value': vsd_points,
                        'vsd_value': vsd_value,
                        'customer_id': move_record.partner_id.id,
                        'employee_id': employee,
                        'servizio': 'Hosting',
                    }
                    entry_exists.write(vals)
        return res
    
    
