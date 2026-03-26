# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class FreightService(models.Model):
    _name = 'freight.service'
    _description = 'Freight Service'
    _rec_name = 'service_id'

    vendor_id = fields.Many2one(
        'res.partner', string='Vendor', required=True, domain="[('supplier_rank','>', 0)]")
    service_id = fields.Many2one('product.template', string='Service',
                                 required=True, domain="[('type','=', 'service')]")
    description = fields.Char(string='Description', required=True)
    quantity = fields.Float('Quantity', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    cost = fields.Float(string='Cost')
    sale = fields.Float(string='Sale')
    freight_route_id = fields.Many2one(
        'freight.route', string='Freight Order Package')
    freight_operation_id = fields.Many2one(
        'freight.operation', string='Freight Operation')

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('freight_route_id') and not values.get('freight_operation_id'):
                route_id = self.env['freight.route'].browse(
                    values.get('freight_route_id'))
                values['freight_operation_id'] = route_id.freight_operation_id.id if route_id and route_id.freight_operation_id else False
        return super(FreightService, self).create(vals_list)

    def action_generate_customer_invoice(self):
        action = {
            'name': 'Create Customer Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'res_model': 'freight.service.invoice.bill',
            'target': 'new',
            'view_id': self.env.ref('bi_freight_management.freight_service_invoice_bill_wizard_view_form').id,
            'context': {'active_ids': self.ids, 'default_freight_service_ids': self.ids, 'default_wizard_type': 'customer_invoice'},
        }
        return action

    def action_generate_vendor_bill(self):
        action = {
            'name': 'Create Vendor Bill',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'res_model': 'freight.service.invoice.bill',
            'target': 'new',
            'view_id': self.env.ref('bi_freight_management.freight_service_invoice_bill_wizard_view_form').id,
            'context': {'active_ids': self.ids, 'default_freight_service_ids': self.ids, 'default_wizard_type': 'vendor_bill'},
        }
        return action
