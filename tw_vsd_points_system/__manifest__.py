# -*- coding: utf-8 -*-

{
    "name": "VSD and Points System",
    "category": 'Project',
    "summary": 'VSD and Points System for employee',
    "description": """
    """,
    "sequence": 1,
    "author": "ticinoWEB",
    "website": "http://www.ticinoweb.tech",
    "version": '13.1',
    "depends": ['project','base', 'hr','hr_timesheet', 'product'],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        'security/security.xml',
        'data/smile_response_mail_template.xml',
        'views/vsd_points_view.xml',
        'views/vsd_points_line_view.xml',
        'views/project_view.xml',
        'views/google_ads_view.xml',
        'views/vsd_setting_view.xml',
        'views/res_config_settings_views.xml',
    ],
    
    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
