# coding: utf-8

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

MONTH_LIST = [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), 
              ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'),('12', 'December')]


YEAR_LIST = [('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'),
              ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'),
              ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'),
              ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'),
              ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'),
              ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), ('2050', '2050'),]



class VsdPointEntry(models.Model):
    _name = 'vsd.point.entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    def unlink(self):
        if not self.env.user.has_group('tw_vsd_points_system.group_delete_vsd_entry'):
            raise UserError(('Deletion is not allowed!'))
        return super(VsdPointEntry,self).unlink()
        

    def action_close(self):
        self.state = 'close'
         
        for line in self.vsd_line_ids:
            line.state = 'close'
             
        self.date_to = fields.Date.today()
#             
    def compute_name(self):
        for rec in self:
            print('rec----',rec)
            if rec.date_from:
                rec.name = 'VSD and Points Value summary from '+str(rec.date_from)
            if rec.date_from and rec.date_to:
                rec.name = 'VSD and Points Value summary from '+str(rec.date_from)+' To '+str(rec.date_to)

    
    name = fields.Char('Name', compute='compute_name')
    date_from = fields.Date('Start Date', required=True)
    date_to = fields.Date('End Date')
    note = fields.Char('Note')
    state = fields.Selection([('open','Open'),('close','Closed')], default='open')
    vsd_line_ids = fields.One2many('vsd.point.entry.line', 'line_id')



class VsdPointEntryLine(models.Model):
    _name = 'vsd.point.entry.line'
    
    
    def auto_set_month_vsd_cron(self):
        records = self.search([('google_ads_month','=',False),('date','!=', False)])
        
        if records:
            for record in records:
                month_no = record.date.month
                print('month_no---',month_no)
                record.google_ads_month = str(month_no)
        
        
        
        records = self.search([('google_ads_year','=',False),('date','!=', False)])
        
        if records:
            for record in records:
                year_no = record.date.year
                print('year_no---',year_no)
                record.google_ads_year = str(year_no)    
    
    
    def unlink(self):
        if not self.env.user.has_group('tw_vsd_points_system.group_delete_vsd_entry'):
            raise UserError(('Deletion is not allowed!'))
        return super(VsdPointEntryLine,self).unlink()
        
    name = fields.Char(related='line_id.name')    
    customer_id = fields.Many2one('res.partner')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    timesheet_id = fields.Many2one('account.analytic.line', string='Timesheet')
    marketing_id = fields.Many2one('online.marketing', string='Marketing Line')
    move_id = fields.Many2one('account.move', string='Move Ref')
    google_ads_year = fields.Selection(YEAR_LIST, string='Year')
    google_ads_month = fields.Selection(MONTH_LIST, string='Month')
    task_id = fields.Many2one('project.task', string='Task')
    project_id = fields.Many2one('project.project', string='Project', related='task_id.project_id')
    points_value = fields.Float(string='Points Value')
    vsd_value = fields.Float(string='VSD Value')
    date = fields.Date('Date')
    user_id = fields.Many2one('res.users', string='Assigned To', related='task_id.user_id')
    state = fields.Selection([('open','Open'),('close','Close')], default='open')
    line_id = fields.Many2one('vsd.point.entry')
    is_smile_bonus = fields.Boolean(string='Smile Bonus', default=False)
    
    servizio =  fields.Selection([('Facebook Marketing','Social Media Marketing'), ('Google Ads','Google Ads'),
                                  ('Email Marketing','Email Marketing'), ('Website','Website'),
                                  ('eCommerce','eCommerce'), ('Odoo','Odoo'), ('Video', 'Video'),
                                  ('Pacchetto Assistenza','Pacchetto Assistenza'),('Grafica','Grafica'),
                                  ('Hosting','Hosting'),('Android','Android/IOS')], 
                                  string="Servizio", related='task_id.servizio', store=True)
    
    

