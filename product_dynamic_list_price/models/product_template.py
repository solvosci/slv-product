# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price_2 = fields.Float(
        string="Price based on company reference pricelist (RRP)",
        tracking=True,
        # company_dependent=True,
        # compute="_compute_list_price_2",
        # store=True
    )

    def _recalculate_list_price_2(self):
        # Initial code (mono pricelist, mono product)
        pricelist = self.env.company.reference_pricelist_id
        for record in self:
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

        # Alternative code, presumabily faster (mono pricelist, multi product): _compute_price_rule
        # pricelist = self.env.company.reference_pricelist_id
        # if pricelist:
        #     results = pricelist._compute_price_rule(
        #         self,
        #         1.0,
        #         date=fields.Date.today()
        #     )
        #     for product in self:
        #         product.list_price_2 = results[product.id][0]
        # else:
        #     for product in self:
        #         product.list_price_2 = product.standard_price



    @api.model
    def recalculate_list_price_2(self):
        # TODO this code is not "company dependent"
        self.env['product.template'].search(
            self._recalculate_list_price_2_domain()
        )._recalculate_list_price_2()

    def _recalculate_list_price_2_domain(self):
        return []

    def action_recalculate_list_price_2(self):
        max_products_count = int(
            self.env["ir.config_parameter"].sudo().get_param(
                "product_dynamic_list_price.recalculate_manual_max_products",
                100
            )
        )
        product_count = len(self.ids)
        if product_count > max_products_count:
            raise UserError(_(
                "You cannot recalculate RRP prices for more than %d product(s),"
                " and %d were selected.\n\n"
                "Please select less products,"
                " or ask an Administrator for increasing current max. products thereshold",
                max_products_count,
                product_count,
            ))
        self._recalculate_list_price_2()
        return True
