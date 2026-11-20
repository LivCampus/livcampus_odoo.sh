from odoo import models, fields


class FreightBooking(models.Model):
    _inherit = "freight.booking"

    company_id = fields.Many2one(
        "res.company", string="Company", required=True, index=True,
        default=lambda self: self.env.company)

    def action_convert_shipment(self):
        # El shipment se crea en la misma compañía del booking
        return super(FreightBooking, self.with_company(self.company_id)).action_convert_shipment()
