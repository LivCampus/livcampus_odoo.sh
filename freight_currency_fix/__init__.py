# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FreightOperation(models.Model):
    """Extiende freight.operation (de bi_freight_management) sin tocar sus
    archivos. Convierte cada factura a la moneda de la compañía antes de
    sumar, en vez de mezclar MXN + USD como si fueran la misma moneda."""
    _inherit = 'freight.operation'

    # Sin copy=False, al Duplicar un shipment Odoo copia el folio actual
    # (name) tal cual en los valores de creación, así que el create()
    # original nunca detecta "New" y nunca genera un folio nuevo por
    # secuencia: el duplicado se queda con el mismo folio que el original.
    name = fields.Char(copy=False)

    def _convert_moves_to_company_currency(self, moves, amount_field):
        company = self.env.company
        company_currency = company.currency_id
        total = 0.0
        for move in moves:
            move_currency = move.currency_id or company_currency
            amount = getattr(move, amount_field) or 0.0
            conv_date = move.invoice_date or fields.Date.context_today(self)
            total += move_currency._convert(amount, company_currency, company, conv_date)
        return total

    @api.depends('freight_service_ids')
    def _compute_expected_receivable(self):
        for record in self:
            moves = self.env['account.move.line'].search(
                [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                lambda l: l.move_id.move_type == 'out_invoice').mapped('move_id')
            record.expected_receivable = record._convert_moves_to_company_currency(
                moves, 'amount_total') if moves else 0.00

    @api.depends('freight_service_ids')
    def _compute_expected_payable(self):
        for record in self:
            moves = self.env['account.move.line'].search(
                [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                lambda l: l.move_id.move_type == 'in_invoice').mapped('move_id')
            record.expected_payable = record._convert_moves_to_company_currency(
                moves, 'amount_total') if moves else 0.00

    @api.depends('freight_service_ids')
    def _compute_actual_receivable(self):
        for record in self:
            moves = self.env['account.move.line'].search(
                [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                lambda l: l.move_id.move_type == 'out_invoice').mapped('move_id')
            paid = record._convert_moves_to_company_currency(moves, 'amount_residual') if moves else 0.00
            record.actual_receivable = record.expected_receivable - paid
            record.receivable_due = paid

    @api.depends('freight_service_ids')
    def _compute_actual_payable(self):
        for record in self:
            moves = self.env['account.move.line'].search(
                [('service_id', 'in', record.freight_service_ids.ids)]).filtered(
                lambda l: l.move_id.move_type == 'in_invoice').mapped('move_id')
            paid = record._convert_moves_to_company_currency(moves, 'amount_residual') if moves else 0.00
            record.actual_payable = record.expected_payable - paid
            record.payable_due = paid

    # --- Comparison between Services (defined) vs Invoiced, shown as a
    # second table on the Accounting tab. Each freight.service line can be
    # in a different currency (currency_id), so every amount is converted
    # to the company currency before summing, same approach used above for
    # invoices via _convert_moves_to_company_currency. ---
    service_sale_total = fields.Float(string='Services Sale', compute='_compute_service_vs_invoiced_totals')
    service_cost_total = fields.Float(string='Services Cost', compute='_compute_service_vs_invoiced_totals')
    service_margin_total = fields.Float(string='Services Margin', compute='_compute_service_vs_invoiced_totals')

    invoiced_sale_total = fields.Float(string='Invoiced Sale', compute='_compute_service_vs_invoiced_totals')
    invoiced_cost_total = fields.Float(string='Invoiced Cost', compute='_compute_service_vs_invoiced_totals')
    invoiced_margin_total = fields.Float(string='Invoiced Margin', compute='_compute_service_vs_invoiced_totals')

    pending_sale_total = fields.Float(string='Pending to Invoice (Sale)', compute='_compute_service_vs_invoiced_totals')
    pending_cost_total = fields.Float(string='Pending to Invoice (Cost)', compute='_compute_service_vs_invoiced_totals')
    pending_margin_total = fields.Float(string='Pending to Invoice (Margin)', compute='_compute_service_vs_invoiced_totals')

    def _convert_amount_to_company_currency(self, amount, from_currency, conv_date=None):
        company = self.env.company
        company_currency = company.currency_id
        currency = from_currency or company_currency
        conv_date = conv_date or fields.Date.context_today(self)
        return currency._convert(amount, company_currency, company, conv_date)

    @api.depends('freight_service_ids.sale', 'freight_service_ids.cost', 'freight_service_ids.quantity',
                 'freight_service_ids.invoiced_sale', 'freight_service_ids.invoiced_cost',
                 'freight_service_ids.currency_id', 'date')
    def _compute_service_vs_invoiced_totals(self):
        for record in self:
            conv_date = record.date or fields.Date.context_today(self)
            service_sale_total = 0.0
            service_cost_total = 0.0
            invoiced_sale_total = 0.0
            invoiced_cost_total = 0.0
            for service in record.freight_service_ids:
                service_sale_total += record._convert_amount_to_company_currency(
                    service.sale * service.quantity, service.currency_id, conv_date)
                service_cost_total += record._convert_amount_to_company_currency(
                    service.cost * service.quantity, service.currency_id, conv_date)
                invoiced_sale_total += record._convert_amount_to_company_currency(
                    service.invoiced_sale, service.currency_id, conv_date)
                invoiced_cost_total += record._convert_amount_to_company_currency(
                    service.invoiced_cost, service.currency_id, conv_date)

            record.service_sale_total = service_sale_total
            record.service_cost_total = service_cost_total
            record.service_margin_total = service_sale_total - service_cost_total

            record.invoiced_sale_total = invoiced_sale_total
            record.invoiced_cost_total = invoiced_cost_total
            record.invoiced_margin_total = invoiced_sale_total - invoiced_cost_total

            record.pending_sale_total = service_sale_total - invoiced_sale_total
            record.pending_cost_total = service_cost_total - invoiced_cost_total
            record.pending_margin_total = record.pending_sale_total - record.pending_cost_total


class FreightBooking(models.Model):
    """Extiende freight.booking (de bi_freight_management) sin tocar sus
    archivos. Mismo problema de folio duplicado que freight.operation."""
    _inherit = 'freight.booking'

    name = fields.Char(copy=False)


class FreightTracking(models.Model):
    """Extiende freight.tracking (de bi_freight_management) sin tocar sus
    archivos. Cambia 'date' de Date a Datetime para poder registrar hora,
    no solo fecha, en cada evento de tracking. No requiere cambios de vista:
    la lista ya usa <field name="date"/>, y Odoo pinta el widget correcto
    según el tipo de campo automáticamente."""
    _inherit = 'freight.tracking'

    date = fields.Datetime(string='Date')


class FreightService(models.Model):
    """Extiende freight.service (de bi_freight_management) sin tocar sus
    archivos. Agrega, por cada línea de servicio, cuánto se ha facturado
    realmente (venta y compra) contra lo que se esperaba cobrar/pagar
    (campos sale/cost x quantity), para poder comparar 'Services' contra
    lo facturado desde la pestaña Accounting del shipment."""
    _inherit = 'freight.service'

    invoiced_sale = fields.Monetary(
        string='Facturado (Venta)', currency_field='currency_id',
        compute='_compute_invoiced_amounts')
    to_invoice_sale = fields.Monetary(
        string='Pendiente por Facturar', currency_field='currency_id',
        compute='_compute_invoiced_amounts')
    sale_invoice_status = fields.Selection(
        [('to_invoice', 'Pendiente'), ('partial', 'Parcial'), ('invoiced', 'Facturado')],
        string='Estado Venta', compute='_compute_invoiced_amounts')

    invoiced_cost = fields.Monetary(
        string='Facturado (Compra)', currency_field='currency_id',
        compute='_compute_invoiced_amounts')
    to_invoice_cost = fields.Monetary(
        string='Pendiente por Facturar (Compra)', currency_field='currency_id',
        compute='_compute_invoiced_amounts')
    cost_invoice_status = fields.Selection(
        [('to_invoice', 'Pendiente'), ('partial', 'Parcial'), ('invoiced', 'Facturado')],
        string='Estado Compra', compute='_compute_invoiced_amounts')

    def _convert_lines_to_currency(self, lines, target_currency):
        company = self.env.company
        total = 0.0
        for line in lines:
            line_currency = line.currency_id or line.move_id.currency_id or company.currency_id
            conv_date = line.move_id.invoice_date or fields.Date.context_today(self)
            total += line_currency._convert(
                line.price_subtotal, target_currency, company, conv_date)
        return total

    @staticmethod
    def _status_from_pending(lines, pending_amount):
        if not lines:
            return 'to_invoice'
        if abs(pending_amount) > 0.01:
            return 'partial'
        return 'invoiced'

    @api.depends('move_line_ids.price_subtotal', 'move_line_ids.currency_id',
                 'move_line_ids.move_id.move_type', 'move_line_ids.move_id.state',
                 'move_line_ids.move_id.invoice_date',
                 'sale', 'cost', 'quantity', 'currency_id')
    def _compute_invoiced_amounts(self):
        for service in self:
            currency = service.currency_id or self.env.company.currency_id
            sale_lines = service.move_line_ids.filtered(
                lambda l: l.move_id.move_type == 'out_invoice' and l.move_id.state == 'posted')
            cost_lines = service.move_line_ids.filtered(
                lambda l: l.move_id.move_type == 'in_invoice' and l.move_id.state == 'posted')

            service.invoiced_sale = service._convert_lines_to_currency(sale_lines, currency)
            service.invoiced_cost = service._convert_lines_to_currency(cost_lines, currency)

            expected_sale = service.sale * service.quantity
            expected_cost = service.cost * service.quantity
            service.to_invoice_sale = expected_sale - service.invoiced_sale
            service.to_invoice_cost = expected_cost - service.invoiced_cost

            service.sale_invoice_status = service._status_from_pending(sale_lines, service.to_invoice_sale)
            service.cost_invoice_status = service._status_from_pending(cost_lines, service.to_invoice_cost)


class FreightServiceInvoiceBill(models.TransientModel):
    """Extiende el wizard freight.service.invoice.bill (de bi_freight_management)
    sin tocar sus archivos. Usa la moneda de las líneas de freight.service
    seleccionadas en vez de la moneda por defecto de Odoo."""
    _inherit = 'freight.service.invoice.bill'

    def create_customer_invoice(self):
        self.ensure_one()
        invoice_line_ids = [(0, None, self._prepare_invoice_line(line))
                             for line in self.freight_service_ids]

        currencies = self.freight_service_ids.mapped('currency_id')
        if len(currencies) > 1:
            raise ValidationError(_(
                'Las líneas de servicio seleccionadas tienen monedas distintas (%s). '
                'Selecciona servicios con la misma moneda.'
            ) % ', '.join(currencies.mapped('name')))
        currency_id = currencies.id if currencies else self.env.company.currency_id.id

        invoice = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice' if self.wizard_type == 'customer_invoice' else 'in_invoice',
            'invoice_date': fields.Date.today(),
            'currency_id': currency_id,
            'line_ids': invoice_line_ids})
        if invoice:
            invoice.action_post()
            return invoice