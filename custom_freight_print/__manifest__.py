{
    'name': 'Custom Freight Print',
    'version': '19.0.1.0.0',
    'summary': 'Add a print button to the cargo reservation and generate a PDF report..',
    'category': 'Industry',
    'author': 'Tendecia UP',
    'depends': ['base', 'bi_freight_management'],
    'data': [
        'views/freight_booking_views_inherit.xml',
        'report/freight_booking_report_templates.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'custom_freight_print/static/src/css/freight_booking_report.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}