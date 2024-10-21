# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

from datetime import datetime

class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    coefficient = fields.Float(string='Coefficient', default=0.0)
    show_coefficient = fields.Boolean("Show Coefficient", default=False)
    price_discount_supplierinfo = fields.Float(string='Supplier Discount', default=0.0)
    base_from_pricelist = fields.Selection(
        selection=[
            ('list_price', 'Sales Price'),
            ('standard_price', 'Cost'),
            ('pricelist', 'Other Pricelist'),
            ("supplierinfo", "Prices based on supplier info"),
        ],
    )

    def _compute_price(self, product, quantity, uom, date, currency):
        result = super()._compute_price(product, quantity, uom, date, currency=currency)

        if isinstance(date, datetime):
            date = date.date()

        discount = 0.0
        seller = None 

        # Price according to the formula
        if self.compute_price == "formula" and self.base == "supplierinfo":

            # Price without discount
            price_without_discount = product.sudo()._get_supplierinfo_pricelist_price(
                self,
                date=date or self.env.context.get("date"),
                quantity=quantity,
            )
            seller = product.sudo()._select_seller(
                partner_id=self.env.context.get("force_filter_supplier_id"),
                quantity=quantity,
                date=date,
            )

            if seller:
                # Get price
                price_discounted = seller._get_supplierinfo_pricelist_price()
                discount = seller.discount or 0.0

                # Apply discount if it exists
                if discount > 0:
                    price_discounted *= (1 - (discount / 100))
                else:
                    price_discounted = price_without_discount  # If not discount, used to price without discount

                # If coefficient is > to 0, applu coefficient to price without discount
                if self.coefficient > 0:
                    result = price_discounted * self.coefficient
                else:
                    # If coeffient = 0, verify if there is discount
                    if discount == 0:
                        # If discount = 0, return 999999
                        result = 999999
                    else:
                        # If there is discount, return price without discount
                        result = price_without_discount
            else:
                # If there isnt  seller, return price without discount
                result = result
        else:
            # If compute_price isnt "formula", return price without discount default
            result = result

        return result


    @api.onchange('base_pricelist_id', 'applied_on', 'categ_id')
    def onchange_base_pricelist_id(self):
        self.coefficient = 0.0
        self.price_discount = 0.0
        self.show_coefficient = False 

        if self.base == 'pricelist' and self.base_pricelist_id:
            if self.applied_on == '2_product_category':
                pricelist_items = self.base_pricelist_id.item_ids.filtered(lambda x: x.categ_id == self.categ_id)
                if pricelist_items:
                    self.coefficient = pricelist_items[0].coefficient
                    self.price_discount_supplierinfo = pricelist_items[0].price_discount
                    self.show_coefficient = True
                    self.base_from_pricelist = pricelist_items[0].base
