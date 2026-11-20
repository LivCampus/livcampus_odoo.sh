from odoo import models


class FreightServiceInvoiceBill(models.TransientModel):
    _inherit = 'freight.service.invoice.bill'

    def create_customer_invoice(self):
        self.ensure_one()
        company = self.freight_operation_id.company_id
        wizard = self.with_company(company) if company else self
        return super(FreightServiceInvoiceBill, wizard).create_customer_invoice()
