{
    'name': 'CRM Freight Bridge Custom',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Hides the native quote button and redirects to Freight Operations.',
    'depends': [
        'crm', 
        'sale_crm', 
        'bi_freight_management'  
    ],
    'data': [
        'views/crm_lead_views_inherit.xml',
        'views/freight_operation_button_views_inherit.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
