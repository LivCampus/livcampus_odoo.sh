# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FreightBookingLine(models.Model):
    _name = 'freight.booking.line'
    _description = 'Freight Booking Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    booking_id = fields.Many2one('freight.booking', string='Booking', required=True, ondelete='cascade')
    display_type = fields.Selection([
        ('line_section', 'Sección'),
        ('line_note', 'Nota'),
    ], default=False, help='Las secciones y notas no representan un producto, solo texto informativo dentro de la lista.')
    name = fields.Text(string='Descripción', help='Texto de la sección o la nota.')
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)])
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=True)
    free_days = fields.Integer(string='Free Days')
    transit_time = fields.Integer(string='Transit Time')
    quantity = fields.Float(string='Quantity', default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price', default=0.0)
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    price_subtotal = fields.Monetary(string='Amount', currency_field='currency_id', compute='_compute_price_subtotal', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('quantity', 'price_unit', 'tax_ids', 'display_type')
    def _compute_price_subtotal(self):
        for line in self:
            if line.display_type:
                line.price_subtotal = 0.0
                continue
            if line.tax_ids:
                taxes = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id or line.env.company.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=line.booking_id.shipper_id or line.booking_id.consignee_id,
                )
                line.price_subtotal = taxes['total_included']
            else:
                line.price_subtotal = line.quantity * line.price_unit

    @api.constrains('product_id', 'display_type')
    def _check_display_type(self):
        for line in self:
            if line.display_type and line.product_id:
                raise ValidationError("Una sección o nota no puede tener un producto asociado.")
            if not line.display_type and not line.product_id:
                raise ValidationError("Debe seleccionar un producto en la línea.")

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