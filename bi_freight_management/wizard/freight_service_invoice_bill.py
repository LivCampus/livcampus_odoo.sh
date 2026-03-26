# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class FreightServiceInvoiceBill(models.TransientModel):
    _name = 'freight.service.invoice.bill'
    _description = "Customer Invoice and Vendor bill from Freight Service Wizard"

    wizard_type = fields.Selection(
        [('customer_invoice', 'Customer Invoice'), ('vendor_bill', 'Vendor Bill')], string='Wizard Type')
    partner_type = fields.Selection(
        [('agent', 'Agent'), ('consignee', 'Consignee'), ('shipper', 'Shipper')], string='Invoice', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    freight_service_ids = fields.Many2many(
        'freight.service', string='Services')

    def _prepare_invoice_line(self, line): 
        return {
            'product_id': line.service_id.product_variant_id.id,
            'service_id': line.id,
            'quantity': line.quantity,
            'price_unit': line.sale if self.wizard_type == 'customer_invoice' else line.cost,
            'name': line.description or line.service_id.product_variant_id.display_name,
            'tax_ids': [(6, 0, line.service_id.product_variant_id.taxes_id.ids)],
            'product_uom_id': line.service_id.product_variant_id.uom_id.id,
        }  

    def create_customer_invoice(self):
        self.ensure_one()
        operation_id = False
        if 'active_domain' in self._context and self._context.get('active_domain') != []:
            operation_id = self._context.get('active_domain')[
                0][2] if 'freight_operation_id' in self._context.get('active_domain')[0][0] else False
        invoice_line_ids = []
        if self.freight_service_ids:
            for line in self.freight_service_ids:
                invoice_line_ids.append((0, None, self._prepare_invoice_line(line)))
        invoice = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice' if self.wizard_type == 'customer_invoice' else 'in_invoice',
            'invoice_date': fields.Date.today(), 
            'line_ids': invoice_line_ids})  
        if invoice:
            invoice.action_post()
            return invoice

    def action_customer_invoice_bill(self):
        self.ensure_one()
        vendors = self.freight_service_ids.mapped('vendor_id') 
        if not len(vendors) == 1:
            ValidationError(_('Please select Same vendor services.'))
        invoice = self.create_customer_invoice() 
        if invoice: 
            name = 'Vendor Bill' if self.wizard_type == 'vendor_bill' else 'Invoice'
            action = {
                'name': _(name),
                'res_id': invoice.id, 
                'view_mode': 'form',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'context': self._context,
            } 
            
            return action
