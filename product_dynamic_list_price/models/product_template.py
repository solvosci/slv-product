# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price_2 = fields.Float(
        string="Price based on company reference pricelist",
        # company_dependent=True,
        # compute="_compute_list_price_2",
        # store=True
    )

    def _recalculate_list_price_2(self):
        # pricelist = self.env.company.reference_pricelist_id
        # for record in self:
        #     if not pricelist:
        #         record.list_price_2 = record.standard_price
        #         continue
        #     price = pricelist._price_get(
        #         product=record,
        #         quantity=1.0,
        #         date=fields.Date.today(),
        #     )[pricelist.id]
        #     if price:
        #         record.list_price_2 = price
        #     else:
        #         record.list_price_2 = record.standard_price

        # Alternative code, presumabily faster (mono pricelist, multi product): _compute_price_rule
        pricelist = self.env.company.reference_pricelist_id
        if pricelist:
            results = pricelist._compute_price_rule(
                self,
                1.0,
                date=fields.Date.today()
            )
            for product in self:
                product.list_price_2 = results[product.id][0]
        else:
            for product in self:
                product.list_price_2 = product.standard_price



    @api.model
    def recalculate_list_price_2(self):
        # TODO this code is not "company dependent"
        self.env['product.template'].search([])._recalculate_list_price_2()
