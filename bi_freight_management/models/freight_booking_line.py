# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class FreightBookingLine(models.Model):
    _name = 'freight.booking.line'
    _description = 'Freight Booking Line'

    booking_id = fields.Many2one('freight.booking', string='Booking', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True, domain=[('sale_ok', '=', True)])
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=True)
    origin_port_id = fields.Many2one('freight.port', string='Origin Port')
    destination_port_id = fields.Many2one('freight.port', string='Destination Port')
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    supplier_ids = fields.Many2many('res.partner', string='Supplier List', compute='_compute_supplier_ids')
    free_days = fields.Integer(string='Free Days')
    transit_time = fields.Integer(string='Transit Time')
    quantity = fields.Float(string='Quantity', default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price', default=0.0)
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    price_subtotal = fields.Monetary(string='Amount', currency_field='currency_id', compute='_compute_price_subtotal', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('product_id')
    def _compute_supplier_ids(self):
        for line in self:
            if line.product_id and line.product_id.seller_ids:
                partner_ids = line.product_id.seller_ids.mapped('partner_id').filtered(lambda p: bool(p)).ids
                line.supplier_ids = [(6, 0, partner_ids)]
            else:
                line.supplier_ids = [(6, 0, [])]

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            return

        product = self.product_id
        self.quantity = 1.0

        uom = getattr(product, 'uom_id', False)
        if uom:
            self.product_uom_id = uom.id
        else:
            self.product_uom_id = False

        self.price_unit = getattr(product, 'lst_price', 0.0) or 0.0

        taxes = getattr(product, 'taxes_id', None)
        if taxes and hasattr(taxes, 'ids'):
            self.tax_ids = [(6, 0, taxes.ids)]
        else:
            self.tax_ids = [(6, 0, [])]

        sellers = getattr(product, 'seller_ids', None)
        if sellers:
            seller = sellers[0] if sellers else False
            if seller and getattr(seller, 'partner_id', False):
                self.supplier_id = seller.partner_id.id
            else:
                self.supplier_id = False
            partner_ids = sellers.mapped('partner_id').filtered(lambda p: bool(p)).ids if hasattr(sellers, 'mapped') else []
            self.supplier_ids = [(6, 0, partner_ids)]
        else:
            self.supplier_id = False
            self.supplier_ids = [(6, 0, [])]

        if hasattr(product, 'free_days'):
            self.free_days = product.free_days
        if hasattr(product, 'transit_time'):
            self.transit_time = product.transit_time

        uom_ids = getattr(product, 'uom_ids', None)
        if uom_ids and hasattr(uom_ids, 'ids'):
            uom_ids = uom_ids.ids
        else:
            uom_ids = []

        return {
            'domain': {
                'product_uom_id': [('id', 'in', uom_ids)] if uom_ids else []
            }
        }
