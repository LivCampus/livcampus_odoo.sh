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
    customer_id = fields.Many2one('res.partner', string='Customer')
    commodity = fields.Char(string='Commodity')

    booking_id = fields.Many2one(
        'freight.booking', 
        string='Booking Asociado', 
        compute='_compute_booking_id',
        store=True
    )

    report_partner_id = fields.Many2one('res.partner', string='Cliente para Reporte', compute='_compute_report_partner')
    report_commodity = fields.Char(string='Commodity para Reporte', compute='_compute_report_commodity')
    
    report_etd_date = fields.Date(string='ETD para Reporte', compute='_compute_report_dates')
    report_eta_date = fields.Date(string='ETA para Reporte', compute='_compute_report_dates')

    @api.depends('name', 'obl')
    def _compute_booking_id(self):
        for record in self:
            booking = self.env['freight.booking'].sudo().search([('freight_operation_id', '=', record.id)], limit=1)
            if not booking and record.obl:
                booking = self.env['freight.booking'].sudo().search([('obl', '=', record.obl)], limit=1)
            record.booking_id = booking.id if booking else False

    @api.depends('customer_id', 'booking_id')
    def _compute_report_partner(self):
        for record in self:
            customer = False
            if record.customer_id:
                customer = record.customer_id
            elif record.booking_id and hasattr(record.booking_id, 'customer_id'):
                if record.booking_id.customer_id:
                    customer = record.booking_id.customer_id
            record.report_partner_id = customer

    @api.depends('commodity', 'booking_id')
    def _compute_report_commodity(self):
        for record in self:
            comm = False
            if record.commodity:
                comm = record.commodity
            elif record.booking_id and hasattr(record.booking_id, 'commodity'):
                if record.booking_id.commodity:
                    comm = record.booking_id.commodity
            if comm:
                record.report_commodity = comm.name if hasattr(comm, 'name') else str(comm)
            else:
                record.report_commodity = 'GEN (General)'

    @api.depends('booking_id')
    def _compute_report_dates(self):
        for record in self:
            etd = False
            eta = False
            
            if record.booking_id:
                if hasattr(record.booking_id, 'etd_date'):
                    etd = record.booking_id.etd_date
                if hasattr(record.booking_id, 'date'):
                    eta = record.booking_id.date
                    
            record.report_etd_date = etd
            record.report_eta_date = eta

    def action_print_house_instruction(self):
        return self.env.ref('custom_freight_print_shipment.action_report_freight_house').report_action(self)
