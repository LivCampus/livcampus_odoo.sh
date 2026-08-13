# -*- coding: utf-8 -*-
{
    'name': 'Custom Freight ',
    'version': '19.0.1.0.0',
    'summary': 'Add custom print button in the All shipments view',
    'category': 'Operations/Logistics',
    'author': 'Tendencia UP',
    'depends': [
        'base',
        'bi_freight_management',
    ],
    'data': [
        'report/freight_house_report.xml',
        'views/freight_operation_views_form_inherit.xml',
        
    ],
    'assets': {
        'web.report_assets_common': [
            'custom_freight_print_shipment/static/src/css/report_assets.css',
        ],
    }, 
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
