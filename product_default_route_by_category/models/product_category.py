# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    default_stock_route_id = fields.Many2one('stock.location.route')
