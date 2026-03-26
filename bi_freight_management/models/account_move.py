# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    service_id = fields.Many2one('freight.service', string='Service')
