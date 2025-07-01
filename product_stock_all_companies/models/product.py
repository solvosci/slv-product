# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_by_company_ids = fields.Many2many(
        'stock.company',
        compute='_compute_stock_by_company_ids',
    )

    @api.depends('stock_quant_ids.inventory_quantity_auto_apply')
    def _compute_stock_by_company_ids(self):
        companies = self.env['res.company'].search([])
        result = []
        for product in self:
            for company in companies:
                quants = self.env['stock.quant'].sudo().search([
                    ('product_id', '=', product.id),
                    ('company_id', '=', company.id),
                    ('location_id.usage', '=', 'internal'),
                ])
                qty = sum(quants.mapped('inventory_quantity_auto_apply'))
                result.append((0, 0, {
                    'product_id': product.id,
                    'company_id': company.id,
                    'quantity_available': qty,
                }))
            product.stock_by_company_ids = result
