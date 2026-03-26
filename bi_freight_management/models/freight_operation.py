# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api


class FreightTrucker(models.Model):
    _name = 'freight.trucker'
    _description = 'Freight Trucker'

    name = fields.Char(string='Name')


class FreightPc(models.Model):
    _name = 'freight.pc'
    _description = 'Freight PC'

    name = fields.Char(string='Name')


class FreightOtherPc(models.Model):
    _name = 'freight.other.pc'
    _description = 'Freight Other PC'

    name = fields.Char(string='Name')


class FreightOperation(models.Model):
    _name = 'freight.operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Freight Operation'

    name = fields.Char(string='Name', required=True,
                       readonly=True, default=lambda self: _('New'))
    type = fields.Selection(
        [('house', 'House'), ('direct', 'Direct'), ('master', 'Master')], string='Type', copy=False)
    selected_type = fields.Boolean(string='Selected Type', default=True)
    stage = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('received', 'Received'), ('in_transit', 'In Transit'),
         ('delivered', 'Delivered')], string='Stage', default='draft', copy=False)
    direction = fields.Selection(
        [('import', 'Import'), ('export', 'Export')], string='Direction', required=True)
    transport = fields.Selection(
        [('air', 'Air'), ('ocean', 'Ocean'), ('land', 'Land')], string='Transport', required=True)
    ocean_shipment_type = fields.Selection(
        [('fcl', 'FCL'), ('lcl', 'LCL')], string='Ocean Shipment Type')
    inland_shipment_type = fields.Selection(
        [('ftl', 'FTL'), ('ltl', 'LTL')], string='Inland Shipment Type')
    shipper_id = fields.Many2one(
        'res.partner', string='Shipper', required=True)
    consignee_id = fields.Many2one(
        'res.partner', string='Consignee', required=True)
    gateway_id = fields.Many2one('res.country', string='Gateway')
    destination_id = fields.Many2one('res.country', string='Destination')
    mawb_no = fields.Char(string='MAWB No')
    airline_id = fields.Many2one('freight.airline', string='Airline')
    flight_no = fields.Char(string='Flight No')
    date = fields.Date(string='Date')
    dangerous_goods = fields.Boolean(string='Dangerous Goods')
    barcode = fields.Char(string='Barcode')
    move_type_id = fields.Many2one('freight.move.type', string='Move Type')
    tracking_no = fields.Char(string='Tracking Number')
    user_id = fields.Many2one('res.users', string='User')
    agent_id = fields.Many2one('res.partner', string='Agent')
    note = fields.Text(string='Notes')
    incoterm_id = fields.Many2one('freight.incoterms', string='Incoterm')
    freight_pc_id = fields.Many2one('freight.pc', string='Freight PC')
    freight_other_pc_id = fields.Many2one(
        'freight.other.pc', string='Other PC')
    loading_port_id = fields.Many2one('freight.port', string='Loading Port')
    discharge_port_id = fields.Many2one(
        'freight.port', string='Discharge Port')
    shipping_line_id = fields.Many2one(
        'res.partner', string='Shipping Line')
    voyage_no = fields.Char(string='Voyage No')
    vessel_id = fields.Many2one('freight.vessel', string='Vessel')
    obl = fields.Char(string='OBL')
    cmr_rwb_pro = fields.Char(string='CMR/RWB#/Pro#')
    from_port_id = fields.Many2one('freight.port', string='From')
    to_port_id = fields.Many2one('freight.port', string='To')
    trucker_id = fields.Many2one('freight.trucker', string='Trucker')
    trucker_no = fields.Char(string='Trucker No')
    freight_order_ids = fields.One2many(
        'freight.order', 'freight_operation_id', string='Freight Orders')
    freight_order_package_ids = fields.One2many('freight.order.package', 'freight_operation_id',
                                                string='Freight Orders Packages')
    freight_route_ids = fields.One2many(
        'freight.route', 'freight_operation_id', string='Routes')
    freight_service_ids = fields.One2many(
        'freight.service', 'freight_operation_id', string='Freight Services')
    declaration_no = fields.Char(string='Declaration Number')
    declaration_date = fields.Date('Declaration Date')
    custom_clearance_date = fields.Date('Customs Clearance Date')
    freight_tracking_ids = fields.One2many(
        'freight.tracking', 'freight_operation_id', string='Freight Tracking')
    expected_receivable = fields.Float(
        string='Expected Receivable', compute='_compute_expected_receivable')
    expected_payable = fields.Float(
        string='Expected Payable', compute='_compute_expected_payable')
    expected_margin = fields.Float(
        string='Expected Margin', compute='_compute_expected_margin')
    actual_receivable = fields.Float(
        string='Actual Receivable', compute="_compute_actual_receivable")
    actual_margin = fields.Float(
        string='Actual Margin', compute='_compute_actual_margin')
    actual_payable = fields.Float(
        string='Actual Payable', compute='_compute_actual_payable')
    receivable_due = fields.Float(string='Receivable Due', readonly=True)
    payable_due = fields.Float(string='Payable Due', readonly=True)
    is_booking = fields.Boolean(string='Booking', readonly=True)
    invoice_count = fields.Integer(
        string='Invoice Count', compute='_compute_invoice_count')
    vendor_bill_count = fields.Integer(
        string='Vendor Bill Count', compute='_compute_vendor_bill_count')
    service_count = fields.Integer(
        string='Service Count', compute='_compute_service_count')
    booking_count = fields.Integer(
        string='Booking Count', compute='_compute_booking_count')
    quotation_count = fields.Integer(
        string='Quotation Count', compute='_compute_quotation_count')
    color = fields.Integer('Color', default=1)

    @api.depends('freight_service_ids')
    def _compute_invoice_count(self):
        for record in self:
            if record.freight_service_ids:
                invoice_ids = self.env['account.move.line'].search(
                    [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                    lambda line: line.move_id.move_type == 'out_invoice').mapped('move_id')
                if invoice_ids:
                    record.invoice_count = len(invoice_ids)
                else:
                    record.invoice_count = 0
            else:
                record.invoice_count = 0

    def _compute_vendor_bill_count(self):
        for record in self:
            if record.freight_service_ids:
                invoice_ids = self.env['account.move.line'].search(
                    [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                    lambda line: line.move_id.move_type == 'in_invoice').mapped('move_id')
                if invoice_ids:
                    record.vendor_bill_count = len(invoice_ids)
                else:
                    record.vendor_bill_count = 0
            else:
                record.vendor_bill_count = 0

    def _compute_service_count(self):
        for record in self:
            if record.freight_service_ids:
                record.service_count = len(record.freight_service_ids)
            else:
                record.service_count = 0

    def _compute_booking_count(self):
        for record in self:
            booking = self.env['freight.booking'].search([('freight_operation_id', '=', record.id)])
            if booking:
                record.booking_count = len(booking)
            else:
                record.booking_count = 0
    
    def _compute_quotation_count(self):
        for record in self:
            order = self.env['sale.order'].search([('freight_operation_id', '=', record.id)])
            if order:
                record.quotation_count = len(order)
            else:
                record.quotation_count = 0

    @api.depends('freight_service_ids')
    def _compute_expected_receivable(self):
        for record in self:
            if record.freight_service_ids:
                out_invoice_ids = self.env['account.move.line'].search(
                    [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                    lambda line: line.move_id.move_type == 'out_invoice').mapped('move_id')
                if out_invoice_ids:
                    record.expected_receivable = sum(out_invoice_ids.mapped(
                        'amount_total')) if out_invoice_ids.mapped('amount_total') else 0.00
                else:
                    record.expected_receivable = 0.00
            else:
                record.expected_receivable = 0.00

    @api.depends('freight_service_ids')
    def _compute_expected_payable(self):
        for record in self:
            if record.freight_service_ids:
                in_invoice_ids = self.env['account.move.line'].search(
                    [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                    lambda line: line.move_id.move_type == 'in_invoice').mapped('move_id')
                if in_invoice_ids:
                    record.expected_payable = sum(in_invoice_ids.mapped(
                        'amount_total')) if in_invoice_ids.mapped('amount_total') else 0.00
                else:
                    record.expected_payable = 0.00
            else:
                record.expected_payable = 0.00

    @api.depends('expected_receivable', 'expected_payable')
    def _compute_expected_margin(self):
        for record in self:
            record.expected_margin = record.expected_receivable - record.expected_payable

    @api.depends('freight_service_ids')
    def _compute_actual_receivable(self):
        for record in self:
            payment_received = 0.00
            if record.freight_service_ids:
                in_invoice_ids = self.env['account.move.line'].search(
                    [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                    lambda line: line.move_id.move_type == 'out_invoice').mapped('move_id')
                if in_invoice_ids:
                    payment_received = sum(in_invoice_ids.mapped(
                        'amount_residual')) if in_invoice_ids.mapped('amount_residual') else 0.00
                    record.actual_receivable = record.expected_receivable - payment_received
                    record.receivable_due = payment_received
                else:
                    record.actual_receivable = 0.00
                    record.receivable_due = 0.00
            else:
                record.actual_receivable = 0.00
                record.receivable_due = 0.00

    @api.depends('freight_service_ids')
    def _compute_actual_payable(self):
        for record in self:
            payment_received = 0.00
            if record.freight_service_ids:
                in_invoice_ids = self.env['account.move.line'].search(
                    [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                    lambda line: line.move_id.move_type == 'in_invoice').mapped('move_id')
                if in_invoice_ids:
                    payment_received = sum(in_invoice_ids.mapped(
                        'amount_residual')) if in_invoice_ids.mapped('amount_residual') else 0.00
                    record.actual_payable = record.expected_payable - payment_received
                    record.payable_due = payment_received
                else:
                    record.actual_payable = 0.00
                    record.payable_due = 0.00
            else:
                record.actual_payable = 0.00
                record.payable_due = 0.00

    @api.depends('actual_receivable', 'actual_payable')
    def _compute_actual_margin(self):
        for record in self:
            record.actual_margin = record.actual_receivable - record.actual_payable

    @api.model_create_multi
    def create(self, vals):
        for value in vals:
            if value.get('name', _('New')) == _('New'):
                prefix = 'HOUSE/'
                if value.get('type') == 'house':
                    prefix = 'HOUSE/'
                if value.get('type') == 'direct':
                    prefix = 'DIRECT/'
                if value.get('type') == 'master':
                    prefix = 'MASTER/'
                value['name'] = prefix + self.env['ir.sequence'].next_by_code(
                    'freight.operation') or _('New')
        record = super(FreightOperation, self).create(vals)
        for rec in record:
            route_operation = 'Main Carriage'
            source = ''
            destination = ''
            routes = False
            if rec.transport == 'air' and rec.gateway_id and rec.destination_id:
                source = rec.gateway_id.name
                destination = rec.destination_id.name
            if rec.transport == 'ocean' and rec.loading_port_id and rec.discharge_port_id:
                source = rec.loading_port_id.name
                destination = rec.discharge_port_id.name
            if rec.transport == 'land' and rec.from_port_id and rec.to_port_id:
                source = rec.from_port_id.name
                destination = rec.to_port_id.name
            self.env['freight.route'].with_context(create_from_operation=True).create(
                {'type': 'pickup', 'freight_operation_id': rec.id,
                 'route_operation': route_operation,
                 'source': source, 'destination': destination,
                 'transport': rec.transport, 'from_port_id': rec.from_port_id.id or False,
                 'to_port_id': rec.to_port_id.id or False, 'date': rec.date, 'trucker_id': rec.trucker_id.id  or False,
                 'gateway_id': rec.gateway_id.id, 'cmr_rwb_pro': rec.cmr_rwb_pro,
                 'trucker_no': rec.trucker_no, 'mawb_no': rec.mawb_no, 'airline_id': rec.airline_id.id or False,
                 'flight_no': rec.flight_no, 'loading_port_id': rec.loading_port_id.id or False,
                 'discharge_port_id': rec.discharge_port_id.id or False, 'shipping_line_id': rec.shipping_line_id.id or False,
                 'voyage_no': rec.voyage_no, 'destination_id': rec.destination_id.id or False,
                 'vessel_id': rec.vessel_id.id or False, 'obl': rec.obl})
            if rec.freight_order_package_ids and rec.freight_route_ids:
                for route in rec.freight_route_ids:
                    for package in rec.freight_order_package_ids:
                        package.freight_route_package_ids = [(0,0, {'freight_package_id': package.id, 'route_id': route.id})]
        return record

    def action_open_booking(self):
        self.ensure_one()
        booking = self.env['freight.booking'].search([('freight_operation_id', '=', self.id)], limit=1)
        if booking:
            return {
                'name': _("Operation Booking"),
                'view_mode': 'form',
                'views': [[False, 'form']],
                'res_id': booking.id,
                'res_model': 'freight.booking',
                'type': 'ir.actions.act_window',
                'context': self._context,
            }

    def action_open_quotation(self):
        self.ensure_one()
        context = {'default_freight_operation_id': self.id, 'default_partner_id': self.shipper_id.id}
        context.update(self._context)
        return {
            'name': _("Freight Quotations"),
            'view_mode': 'list,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('freight_operation_id', '=', self.id)],
        }

    def action_open_services(self):
        self.ensure_one()
        context = {'default_freight_operation_id': self.id}
        context.update(self._context)
        return {
            'name': _("Freight Services"),
            'view_mode': 'list,form',
            'res_model': 'freight.service',
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('freight_operation_id', '=', self.id)],
        }

    def action_open_invoices(self):
        invoice_ids = self.env['account.move.line'].search(
            [('service_id', 'in', self.freight_service_ids.ids)]).filtered(
            lambda line: line.move_id.move_type == 'out_invoice').mapped('move_id')
        action = {
            'name': _('Customer Invoice'),
            'views': [[False, 'list']],
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
            'domain': [('id', 'in', invoice_ids.ids)],
        }
        return action

    def action_open_vendor_bill(self):
        invoice_ids = self.env['account.move.line'].search(
            [('service_id', 'in', self.freight_service_ids.ids)]).filtered(
            lambda line: line.move_id.move_type == 'in_invoice').mapped('move_id')
        action = {
            'name': _('Customer Invoice'),
            'views': [[False, 'list']],
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
            'domain': [('id', 'in', invoice_ids.ids)],
        }
        return action

    def action_generate_packages_from_orders(self):
        self.ensure_one()
        for order_line in self.freight_order_ids:
            if not order_line.freight_order_package_id:
                freight_order_package_id = self.env['freight.order.package'].create(
                    {'description': order_line.description, 'package_id': order_line.package_id.id,
                     'quantity': order_line.quantity, 'operation_value_id': order_line.operation_value_id.id,
                     'volume': order_line.volume, 'gross_weight': order_line.gross_weight,
                     'freight_order_id': order_line.id, 'freight_operation_id': self.id})
                if freight_order_package_id:
                    order_line.freight_order_package_id = freight_order_package_id.id
