# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _set_categ_id_from_route(self, vals):
        if vals.get('route_ids'):
            if vals["route_ids"][0][0] == 6 and len(vals["route_ids"][0][2]):
                return self.categ_id.search([
                    ('default_stock_route_id', 'in', vals.get('route_ids')[0][2])
                ], limit=1).id
        return False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            categ_id = self._set_categ_id_from_route(vals)
            if categ_id:
                vals["categ_id"] = categ_id
        templates = super(ProductTemplate, self).create(vals_list)
        return templates

    def write(self, vals):
        categ_id = self._set_categ_id_from_route(vals)
        if categ_id:
            vals["categ_id"] = categ_id
        return super().write(vals)

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id.default_stock_route_id:
            opposite_route = self.env['product.category'].search([
                ('id', '!=', self.categ_id.id),
                ('default_stock_route_id', '!=', False)
            ]).default_stock_route_id.id
            self.route_ids = [(3, r) for r in self.route_ids.ids if r == opposite_route]
            self.route_ids = [(4, self.categ_id.default_stock_route_id.id)]
