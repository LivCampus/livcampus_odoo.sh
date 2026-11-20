from odoo import models, fields


class FreightOperation(models.Model):
    _inherit = "freight.operation"

    company_id = fields.Many2one(
        "res.company", string="Company", required=True, index=True,
        default=lambda self: self.env.company)
