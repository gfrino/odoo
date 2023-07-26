# coding: utf-8

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError



class ProjectProjectInh(models.Model):
    _inherit = 'project.project'
    _description = 'Project Inherit VSD'


    is_google_ads_project = fields.Boolean(string='Is Google Ads Project', default=False)



class ProjectTaskInh(models.Model):
    _inherit = 'project.task'
    
    
    def action_update_vsd(self):
        if self.planned_hours <= 0:
            raise UserError('Planned Hours must be greater than zero!')
        
        for timesheet in self.timesheet_ids:
            entry_exists = self.env['vsd.point.entry.line'].search([('timesheet_id','=',timesheet.id)])
        
            if not entry_exists:
                vals = {
                    'task_id': self.id,            
                    'points_value':(self.points_value / self.planned_hours) * timesheet.unit_amount,
                    'vsd_value': (self.vsd_value / self.planned_hours) * timesheet.unit_amount,
                    'customer_id':self.partner_id.id,
                    'employee_id':timesheet.employee_id.id,
                    'date': fields.Date.today(),
                    'timesheet_id': timesheet.id,
                }
                record = self.env['vsd.point.entry.line'].create(vals)
                
                
                found = False
                
                vsd_rec = self.env['vsd.point.entry'].search([('state','=','open')])
                
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
                    'employee_id':timesheet.employee_id.id,
                    'points_value':(self.points_value / self.planned_hours) * timesheet.unit_amount,
                    'vsd_value': (self.vsd_value / self.planned_hours) * timesheet.unit_amount,
                }
                entry_exists.write(vals)
    
    
    def mark_as_done(self):
        employee = self.env['hr.employee'].search([('user_id','=',self.user_id.id)], order='id desc', limit=1)

        vals = {
            'task_id': self.id,            
            'points_value':self.points_value,
            'vsd_value': self.vsd_value,
            'customer_id':self.partner_id.id,
            'employee_id':employee.id,
            'date': fields.Date.today(),
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
        
        
        
        
        marketing_ids = self.env['online.marketing'].search([('omtask_id','=',self.id)])
        if marketing_ids:
            for marketing_id in marketing_ids:
                marketing_id.activity_id.action_done()
                
                
        self.vsd_status = 'done'
        
    
    @api.onchange('servizio')
    def onchange_servizio(self):
        if self.servizio:
            if self.servizio == 'Website':
                self.points_value = 1
                self.vsd_value = 1250
            elif self.servizio == 'eCommerce':
                self.points_value = 4
                self.vsd_value = 4850
            elif self.servizio == 'Odoo':
                self.points_value = 1
                self.vsd_value = 500
            elif self.servizio == 'Video':
                self.points_value = 1
                self.vsd_value = 1250
            elif self.servizio == 'Facebook Marketing':
                self.points_value = 9
                self.vsd_value = 3300
            else:
                self.points_value = 0
                self.vsd_value = 0
    
    
    @api.constrains('planned_hours')
    def constraint_on_planned_hours(self):
        if self.servizio:
            if self.servizio == 'Pacchetto Assistenza':
                if self.planned_hours <= 0:
                    raise UserError('Planned Hours must be greater than zero!')        
    
    @api.depends('vsd_value')
    @api.onchange('vsd_value')
    def onchange_vsd_value(self):
        vsd_value_amount = float(self.env['ir.config_parameter'].sudo().get_param('vsd_value_amount'))
        self.points_value = self.vsd_value / vsd_value_amount
    
    @api.model
    def create(self, vals):
        if 'vsd_value' not in vals:
            vals['vsd_value'] = 0
            
        vsd_value_amount = float(self.env['ir.config_parameter'].sudo().get_param('vsd_value_amount'))

        if vsd_value_amount <= 0:
            raise UserError('VSD Value Amount in Configurations must be greater than zero!')
        
        vals['points_value'] = vals['vsd_value'] / vsd_value_amount


        rec = super(ProjectTaskInh, self).create(vals)
        if rec.servizio:
            if rec.servizio == 'Pacchetto Assistenza':
                if rec.planned_hours <= 0:
                    raise UserError('Planned Hours must be greater than zero!') 
        
        return rec 
    
    
    def write(self,vals):
        rec = super(ProjectTaskInh, self).write(vals)
        vsd_value_amount = float(self.env['ir.config_parameter'].sudo().get_param('vsd_value_amount'))

        if vsd_value_amount <= 0:
            raise UserError('VSD Value Amount in Configurations must be greater than zero!')
        
        if 'vsd_value' in vals:
            self.points_value = vals['vsd_value'] / vsd_value_amount
        
        if 'servizio' in vals:
            if self.servizio == 'Pacchetto Assistenza':
                if self.planned_hours <= 0:
                    raise UserError('Planned Hours must be greater than zero!')
        return rec
    
    
    def compute_timesheet(self):
        for rec in self:
            if rec.timesheet_ids:
                rec.is_added_timsheet = True
            else:
                rec.is_added_timsheet = False
                
    
    def days_between_dates(self, date_from, date_to):
        delta = date_from - date_to
        return abs(delta.days)+1
    
    
    def compute_planned_total_days(self):
        for rec in self:
            if rec.gantt_start_date and rec.gantt_stop_date:
                start_dt = rec.gantt_start_date.date()
                stop_dt = rec.gantt_stop_date.date()
                rec.planned_total_days = rec.days_between_dates(start_dt, stop_dt)
                
            else:
                rec.planned_total_days = 0
                
                
            if rec.is_exception:
                if rec.ex_start_date and rec.ex_end_date:
                    rec.ex_total_days = rec.days_between_dates(rec.ex_start_date, rec.ex_end_date)
                else:
                    rec.ex_total_days = 0
            else:
                rec.ex_total_days = 0
                
    
    @api.constrains('ex_start_date','ex_end_date')
    def constraint_ex_dates(self):
        if self.is_exception:
            if self.ex_start_date < self.gantt_start_date.date() or self.ex_start_date > self.gantt_stop_date.date():
                raise UserError('Exception dates must be in between planned dates!')
            if self.ex_end_date > self.gantt_stop_date.date():
                raise UserError('Exception dates must be in between planned dates!')
            if self.ex_end_date < self.ex_start_date:
                raise UserError('Exception End Date must be greater than Exception Start Date!')
            
    
    def compute_latest_calculated_vsd(self):
        for rec in self:
            entry_exists = self.env['vsd.point.entry.line'].search([('task_id','=',rec.id)], order='id desc', limit=1)    
            
            if entry_exists:
                rec.cal_points_value = entry_exists.points_value
                rec.cal_vsd_value = entry_exists.vsd_value
            else:
                rec.cal_points_value = 0
                rec.cal_vsd_value = 0  
                
    
    @api.depends('daily_budget', 'vsd_value')
    def compute_daily_budget(self):
        for rec in self:
            if rec.planned_total_days > 0:
                rec.daily_budget = (rec.budget_percentage * rec.vsd_value) / rec.planned_total_days 
            else:
                rec.daily_budget = 0
                  
                
    servizio =  fields.Selection([('Facebook Marketing','Social Media Marketing'), ('Google Ads','Google Ads'),
                                  ('Email Marketing','Email Marketing'), ('Website','Website'),
                                  ('eCommerce','eCommerce'), ('Odoo','Odoo'), ('Video', 'Video'),
                                  ('Pacchetto Assistenza','Pacchetto Assistenza'),('Grafica','Grafica'),
                                  ('Hosting','Hosting'),('Android','Android/IOS')], string="Servizio", required=True)
    
    points_value = fields.Float(string='Points Value', default=0.0)
    vsd_value = fields.Float(string='VSD Value')
    daily_budget = fields.Float(string='Daily Budget', compute='compute_daily_budget')
    budget_percentage = fields.Float(string='Budget Percent', default=0.35)
    budget_percent = fields.Float(string='Budget Percent tobe removed')
    vsd_status =  fields.Selection([('inprogress','In Progress'), ('done','Done')], default='inprogress')
    is_added_timsheet = fields.Boolean(compute='compute_timesheet')
    planned_total_days = fields.Integer(string='Days', compute='compute_planned_total_days')
    is_exception = fields.Boolean(string='Enable Exception', default=False)
    ex_start_date = fields.Date(string='Exception Start Date')
    ex_end_date = fields.Date(string='Exception End Date')
    ex_points_value = fields.Float(string='Ex VSD Points')
    ex_vsd_value = fields.Float(string='Ex VSD Value')
    ex_total_days = fields.Integer(string='Ex Days', compute='compute_planned_total_days')
    
    #show calculated vsd and value fields
    cal_points_value = fields.Float(string='Calculated Points Value', compute='compute_latest_calculated_vsd')
    cal_vsd_value = fields.Float(string='Calculated VSD Value', compute='compute_latest_calculated_vsd')
    
    
    # tab fields
    cartella_kdrive = fields.Boolean('Cartella kDrive')
    consulenza = fields.Boolean('Consulenza')
    testing = fields.Boolean('Testing')
    mailpoet_setup = fields.Boolean('Mailpoet Setup')
    logo = fields.Boolean('Logo')
    favicon = fields.Boolean('Favicon')
    testi = fields.Boolean('Testi')
    foto_di_qualita = fields.Boolean('Foto di qualità')
    color_palette = fields.Boolean('Color Palette')
    scegliere_font = fields.Boolean('Scegliere Font')
    bozza_sito = fields.Boolean('Bozza sito')
    responsive = fields.Boolean('Responsive')
    impostare_campagna = fields.Boolean('Impostare la Campagna')
    integrazione_facebook = fields.Boolean(string="Integrazione del sito web con Facebook")
    google_my_business = fields.Boolean('Google My Business')
    seo = fields.Boolean('SEO')
    search_console = fields.Boolean('Search Console')           
    client_review = fields.Boolean('Client review') 
    correzioni = fields.Boolean('Correzioni')    
    email_setup = fields.Boolean('Email Setup')
    cliente_soddisfatto = fields.Boolean('Cliente soddisfatto')  
    valutazione_taff_ticino = fields.Selection([('Normal','Normal'), ('Low','Low'), ('High','High'), ('Very High','Very High'), ('Super High','Super High'), ('Mega High','Mega High')], string='Valutazione dello staff ticinoWEB')      
    data_di_completamento = fields.Date('Data di Completamento')       
    inviare_saldo = fields.Boolean('Inviare Saldo')
    pubblicare_blog = fields.Boolean('Pubblicare Blog')
    pianificazione_cliente = fields.Boolean('Pianificazione Mensile delle campagne con il Cliente')
    design_archivio_prodotti = fields.Boolean('Design Archivio Prodotti')  
    design_pagina_rodotto = fields.Boolean('Design Pagina Prodotto')  
    cart_checkout = fields.Boolean('Cart & Checkout')
    termini_condizioni = fields.Boolean('Termini & Condizioni')
    bozza_video = fields.Boolean('Bozza Video')
    server_setup = fields.Boolean('Server Setup')
    
    campaign_goals = fields.Text('Campaign Goals')
    target_audience = fields.Text('Target Audience Analysis')
    competition_research = fields.Text('Competition Research')
    social_media_audit = fields.Text('Social Media Audit')
    google_ads_audit = fields.Text('Google Ads Audit')

    
    
    
    