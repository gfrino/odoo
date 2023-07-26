# coding: utf-8

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RatingRatingInh(models.Model):
    _inherit = 'rating.rating'
    _description = 'rating rating in VSD'
    
    
    def write(self, values):
        print('inside rating writee---')
        rec = super(RatingRatingInh, self).write(values)
        print('self.rating_text in writeeee 222-----',self.rating_text)
        
        
        if self.rating_text == 'satisfied':
            print('rec.rating_text--------',self.rating_text)
            if self.res_model == 'project.task' and self.parent_res_model == 'project.project':
                task_id = self.env['project.task'].search([('id','=',self.res_id),('project_id','=',self.parent_res_id)], order="id desc", limit=1)
                print('task_id--------',task_id)
                if task_id:
                    smile_entry_exists = self.env['vsd.point.entry.line'].search([('task_id','=',task_id.id),('is_smile_bonus','=',True)])
                    
                    if not smile_entry_exists:
                        print('inside smile entry exists')
                        employee = self.env['hr.employee'].search([('user_id','=',task_id.user_id.id)], order='id desc', limit=1)
        
                        vals = {
                            'task_id': task_id.id,            
                            'points_value': 0.25,
                            'vsd_value': 0.0,
                            'customer_id':task_id.partner_id.id,
                            'employee_id':employee.id,
                            'date': fields.Date.today(),
                            'is_smile_bonus': True,
                        }
                        record = self.env['vsd.point.entry.line'].create(vals)
                        
                        found = False
                        
                        vsd_rec = self.env['vsd.point.entry'].search([('state','=','open')])
                        
                        if vsd_rec:
                            record.line_id = vsd_rec.id
                        else:
                            vals = {
                                'date_from':record.date,
                            }
                            p_record = self.env['vsd.point.entry'].create(vals)
                            record.line_id = p_record.id
                        self.send_smile_response_mail()
        return rec
    

    
    def send_smile_response_mail(self):
        company_id = self.env['res.company'].browse(1)
        
        
        ctx = {}
        if self.partner_id.lang == 'it_IT':
            ctx['subject'] = 'Scrivi una recensione su ticinoWEB!'
        elif self.partner_id.lang == 'de_DE':
            ctx['subject'] = 'Schreiben Sie eine Bewertung auf ticinoWEB!'
        else:
            ctx['subject'] = 'Write a review on ticinoWEB!'
        
        ctx['email_from'] = company_id.email
        ctx['email_to'] = self.partner_id.email
        ctx['customer_name'] = self.partner_id.name
        ctx['lang'] = self.partner_id.lang
        template = self.env.ref('tw_vsd_points_system.smile_response_email_template')
        template.with_context(ctx).sudo().send_mail(self.id, force_send=True, raise_exception=False)
        
        
        
        