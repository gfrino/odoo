# coding: utf-8

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.addons.test_convert.tests.test_env import field
from calendar import monthrange
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta, TH, FR



MONTH_LIST = [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'),
              ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'),('12', 'December')]


YEAR_LIST = [('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'),
              ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'),
              ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'),
              ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'),
              ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'),
              ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), ('2050', '2050'),]



class VsdMonthlyModel(models.Model):
    _name = 'vsd.yearly'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "VSD Monthly"


    @api.model
    def create(self, vals):
        rec = super(VsdMonthlyModel, self).create(vals)
        if rec.name:
            for i in range(0,12):
                print('index=====',MONTH_LIST[i])

                date_time_str = str(rec.name)+'-'+str(MONTH_LIST[i][0])+'-'+str(1)+' 00:00:00'
                date_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                date_to = date_obj.date()

#                 if date_to.day == 'Thursday':
#                     date_to = date_to
                print('------------before----------------')
                print(date_to)
                if date_to.strftime("%A") == 'Friday':
                    print('yesss friday')
                    date_from = date_to
                else:
                    print('not friday')
                    date_from = date_to + relativedelta(months=-1)
                    date_from = self.get_friday(date_from)

                date_to = self.get_thursday(date_to)
                print('date_from----',date_from)
                print('date_to----',date_to)

#                 raise UserError('STOP')
                vals = {
                    'year': rec.name,
                    'name':MONTH_LIST[i][0],
                    'date_start': date_from,
                    'date_end': date_to,
                    'parent_id': rec.id,
                    }
                print('valsss',vals)
                record = self.env['vsd.monthly'].create(vals)
        return rec

    def get_first_date_month(self, dt):
        first_date = dt.replace(day=1)
        return first_date.day

    def get_thursday(self, dt):
        last_thursday = dt + relativedelta(day=31, weekday=TH(-1))
        return last_thursday


    def get_friday(self, dt):
        last_friday = dt + relativedelta(day=31, weekday=FR(-1))
        return last_friday


    def action_close(self):
        if self.line_ids:
            for line in self.line_ids:
                if line.state == 'open':
                    raise UserError(('Please make sure state of all months must be close!'))

        self.state = 'close'


    name = fields.Selection(YEAR_LIST, string='Year', required=True)
    state = fields.Selection([('open','Open'),('close','Closed')], default='open')
    line_ids = fields.One2many('vsd.monthly', 'parent_id', string='Months', ondelete='cascade')

    _sql_constraints = [
    ('name_uniq', 'unique (name)', "Same Year already exists!"),
    ]



class VsdMonthlyModelLine(models.Model):
    _name = 'vsd.monthly'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "VSD Monthly Line"


    def days_in_month(self, year, month):
        a = monthrange(year, month)

        if date.today().month == month and date.today().year == year:
            tot_days = date.today().day
        else:
            tot_days = a[1]

        return tot_days

#         return a[1]


    def days_between_dates(self, date_from, date_to):
        delta = date_from - date_to
        return abs(delta.days)+1


    def get_month_year_list(self, date_from, date_to):
        listt = []

        if date_from.day != date_to.day:
            day = date_from.day
            month = date_to.month
            year = date_to.year

            date_time_str = str(year)+'-'+str(month)+'-'+str(day)+' 00:00:00'
            date_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_to = date_obj.date()


        cur_date = start = datetime.strptime(str(date_from), '%Y-%m-%d').date()
        end = datetime.strptime(str(date_to), '%Y-%m-%d').date()

        while cur_date <= end:
            listt.append(str(cur_date)[:-3])
            cur_date += relativedelta(months=1)
        return listt


    def get_date_list(self, df, dt):
        date_list = []
        for rec in self:
            delta = dt - df
            for i in range(delta.days + 1):
                day = df + timedelta(days=i)
                date_list.append(str(day))
                i = i + 1
        return date_list


    def action_update_vsd_google(self):
        print('month number-----',self.name)
        project_ids = self.env['project.project'].search([('is_google_ads_project','=',True)])

        for project_id in project_ids:
            task_ids = self.env['project.task'].search([('project_id','=', project_id.id)])

            for task_id in task_ids:
                if task_id.gantt_start_date and date.today() >= task_id.gantt_start_date.date() and task_id.gantt_stop_date:
                    print('-------------------------------------------------------')
                    date_from = task_id.gantt_start_date.date()
                    date_to = task_id.gantt_stop_date.date()
                    total_days = self.days_between_dates(date_from, date_to)
                    to_be_minus1 = to_be_minus2 = 0

                    if (self.date_start >= date_from and self.date_start <= date_to) or (self.date_end >= date_from and self.date_end <= date_to) or (date_from >= self.date_start and date_to <= self.date_end):
                        print('task---------',task_id.name)

#                         if self.date_end.month == date_to.month:
                        if date_to < self.date_end:
                            to_be_minus1 = self.days_between_dates(date_to, self.date_end) - 1
                            print('to_be_minus1-----',to_be_minus1)

                        if date_from > self.date_start:
                            to_be_minus2 = self.days_between_dates(self.date_start, date_from) - 1
                            print('to_be_minus2-----',to_be_minus2)

                        to_be_minus = to_be_minus1 + to_be_minus2


                        if date_from >= self.date_start and date_to <= self.date_end:
                            print('iffff')
                            if date.today() < self.date_end:
                                final_days = abs(self.days_between_dates(date_from, date.today()))
                            else:
                                final_days = abs(self.days_between_dates(date_from, date_to))

                        elif date_to > self.date_start and date_to < self.date_end:
                            print('elifffff')
                            final_days = abs(self.days_between_dates(self.date_start, date_to))

                        else:
                            print('elseeee')
                            if date.today() < self.date_end:
                                print('iffff')
                                final_days = abs(self.days_between_dates(self.date_start, date.today()) - to_be_minus)
                            else:
                                final_days = abs(self.days_between_dates(self.date_start, self.date_end) - to_be_minus)

                        print('final_days---------',final_days)


                        """Exception Code Start Here"""
                        #checking if exception days
                        ex_vsd_value = ex_vsd_points = 0
                        ex_days_count = 0
                        if task_id.is_exception:
                            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            ex_start_date = task_id.ex_start_date
                            ex_end_date = task_id.ex_end_date

                            if date.today() >= ex_start_date and date.today() <= ex_end_date:
                                ex_total_days = self.days_between_dates(ex_start_date, ex_end_date)
                                exception_dates = self.get_date_list(task_id.ex_start_date, date.today())

                                for ex_date in exception_dates:
                                    if ex_date >= str(self.date_start) and ex_date <= str(self.date_end):
                                        ex_days_count += 1

                                ex_vsd_value = (task_id.ex_vsd_value / ex_total_days) * ex_days_count
                                ex_vsd_points = (task_id.ex_points_value / ex_total_days) * ex_days_count

                        final_days = final_days - ex_days_count
                        vsd_value = ((task_id.vsd_value / total_days) * final_days) + ex_vsd_value
                        vsd_points = ((task_id.points_value / total_days) * final_days) + ex_vsd_points
                        print('vsd_value----',vsd_value)
                        print('vsd_points----',vsd_points)


                        """Creating entry to VSD"""
                        employee = self.env['hr.employee'].search([('user_id', '=', task_id.user_id.id)], order='id desc', limit=1)
                        entry_exists = self.env['vsd.point.entry.line'].search([('task_id', '=', task_id.id),
                                                                                ('google_ads_month','=',self.name),
                                                                                ('google_ads_year','=',self.parent_id.name),
                                                                                ('is_smile_bonus', '=', False),
                                                                                ('is_helpdesk_ticket', '=', False)])

                        if not entry_exists:
                            vals = {
                                'task_id': task_id.id,
                                'google_ads_month': self.name,
                                'google_ads_year': self.parent_id.name,
                                'points_value': vsd_points,
                                'vsd_value': vsd_value,
                                'customer_id': task_id.partner_id.id,
                                'employee_id': employee.id,
                                'date': fields.Date.today(),
                            }
                            record = self.env['vsd.point.entry.line'].create(vals)

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

                            task_id.vsd_id = self.id

                        else:
                            vals = {
                                'points_value': vsd_points,
                                'vsd_value': vsd_value,
                                'customer_id': task_id.partner_id.id,
                                'employee_id': employee.id,
                            }
                            entry_exists.write(vals)



    def action_close(self):
        self.date_close = date.today()
        self.state = 'close'



    parent_id = fields.Many2one('vsd.yearly', string='Parent', ondelete='cascade')
    name = fields.Selection(MONTH_LIST, string='Month')
    year = fields.Selection(YEAR_LIST, string='Year')
    state = fields.Selection([('open','Open'),('close','Close')], default='open')
    date_close = fields.Date(string='Closing Date')

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    task_ids = fields.One2many('project.task', 'vsd_id', sting='Related Tasks')



class ProjectTaskInh(models.Model):
    _inherit = 'project.task'

    vsd_id = fields.Many2one('vsd.monthly', string='VSD ID')







