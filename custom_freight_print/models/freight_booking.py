from odoo import models, fields, api

class FreightBooking(models.Model):
    _inherit = 'freight.booking'

    customer_id = fields.Many2one(
        'res.partner', string='Customer',
        help='Customer of the quotation. Used to print the quotation PDF (company, attention and language).')

    commodity = fields.Char(string='Commodity')

    intructions_hbl  = fields.Char(string='Instruction for HBL', help='HBL is must with emission at destination')

    mbl_destination = fields.Char(string='MBL must be SWB or with insuance at destination')

    house_number = fields.Char(string='House Number')

    etd_date = fields.Date(string='ETD')

    freight_payable = fields.Selection([
    ('collect', 'Collect'),
    ('prepaid', 'Prepaid')
], string="Freight Payable")

    add_total = fields.Boolean(string='Agregar total', default=True, help='Si está activo, se incluirá el total en la cotización (Freight Quotation).')
    
    quote_validity_date = fields.Date(string='Vigencia de la Cotización')

    def action_button_printreport_freight(self):
        return self.env.ref('custom_freight_print.action_report_freight_booking').report_action(self)
    
    def action_button_print_quotation(self):
        return self.env.ref('custom_freight_print.action_report_freight_quotation').report_action(self)
    
    
    def action_convert_shipment(self):
       result = super(FreightBooking, self).action_convert_shipment()
       for booking in self:
           if booking.etd_date and booking.freight_operation_id:
               if 'etd_date' in booking.freight_operation_id._fields:
                   booking.freight_operation_id.write({'etd_date': booking.etd_date})
       return result


class FreightBookingLine(models.Model):
    _inherit = 'freight.booking.line'

    booking_currency_id = fields.Many2one(
        'res.currency', related='booking_id.currency_id', string='Booking Currency')

    price_unit_converted = fields.Monetary(
        string='Unit Price (Converted)', currency_field='booking_currency_id',
        compute='_compute_price_converted',
        help="Unit price converted to the Booking's currency using today's exchange rate. Used for printing the quotation.")

    price_subtotal_converted = fields.Monetary(
        string='Subtotal (Converted)', currency_field='booking_currency_id',
        compute='_compute_price_converted',
        help="Subtotal converted to the Booking's currency using today's exchange rate. Used for printing the quotation.")

    @api.depends('price_unit', 'price_subtotal', 'currency_id', 'booking_id.currency_id')
    def _compute_price_converted(self):
        for line in self:
            company = line.env.company
            target_currency = line.booking_id.currency_id or company.currency_id
            source_currency = line.currency_id or target_currency
            conv_date = fields.Date.context_today(line)
            line.price_unit_converted = source_currency._convert(
                line.price_unit or 0.0, target_currency, company, conv_date)
            line.price_subtotal_converted = source_currency._convert(
                line.price_subtotal or 0.0, target_currency, company, conv_date)