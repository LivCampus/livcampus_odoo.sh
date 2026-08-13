from odoo import models, fields, api

class FreightOperation(models.Model):
    _inherit = 'freight.operation'

    report_package_ids = fields.One2many(
        'freight.order.package', 
        'freight_operation_id', 
        string='Paquetes para Reporte'
    )

    date_create_shipment = fields.Datetime(
        string='Date create shipment',
        related='create_date',
        readonly=True,
        store=True
    )

    release_type = fields.Char(string='Release Type')

    def action_print_house_instruction(self):
        return self.env.ref('custom_freight_print_shipment.action_report_freight_house').report_action(self)
