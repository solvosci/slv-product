# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price_2 = fields.Float(
        compute="_compute_list_price_2",
        store=True
    )

    def _compute_list_price_2(self):
        for record in self:
            pricelist = self.env.company.reference_pricelist_id
            if not pricelist:
                record.list_price_2 = record.standard_price
                continue
            price = pricelist._price_get(
                product=record,
                quantity=1.0,
                date=fields.Date.today(),
            )[pricelist.id]
            if price:
                record.list_price_2 = price
            else:
                record.list_price_2 = record.standard_price

    def recalculate_list_price_2(self):
        self.env['product.template'].search([])._compute_list_price_2()
