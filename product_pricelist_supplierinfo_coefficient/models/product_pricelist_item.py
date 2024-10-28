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

    coefficient_from_pricelist = fields.Float(
        string='Supplier Coefficient', compute="_compute_coeff_and_discount", store=True
    )
    price_discount_supplierinfo = fields.Float(
        string='Supplier Discount', compute="_compute_coeff_and_discount", store=True
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
    
    @api.depends('base_pricelist_id.item_ids.coefficient', 'base_pricelist_id.item_ids.price_discount', 'applied_on', 'categ_id', 'product_tmpl_id', 'product_id')
    def _compute_coeff_and_discount(self):
        for record in self:
            record.coefficient_from_pricelist = 0.0
            record.price_discount_supplierinfo = 0.0
            record.show_coefficient = False

            if record.base == 'pricelist' and record.base_pricelist_id:
                if record.applied_on == '2_product_category':
                    pricelist_items = record.base_pricelist_id.item_ids.filtered(
                        lambda x: x.categ_id == record.categ_id
                    )
                    if pricelist_items:
                        record.coefficient_from_pricelist = pricelist_items[0].coefficient
                        record.price_discount_supplierinfo = pricelist_items[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = pricelist_items[0].base

                elif record.applied_on == '1_product':
                    pricelist_items = record.base_pricelist_id.item_ids.filtered(
                        lambda x: x.product_tmpl_id == record.product_tmpl_id
                    )
                    if pricelist_items:
                        record.coefficient_from_pricelist = pricelist_items[0].coefficient
                        record.price_discount_supplierinfo = pricelist_items[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = pricelist_items[0].base
                        
                elif record.applied_on == '0_product_variant':
                    pricelist_items = record.base_pricelist_id.item_ids.filtered(
                        lambda x: x.product_id == record.product_id
                    )
                    if pricelist_items:
                        record.coefficient_from_pricelist = pricelist_items[0].coefficient
                        record.price_discount_supplierinfo = pricelist_items[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = pricelist_items[0].base

                elif record.applied_on == '3_global':
                    pricelist_items = record.base_pricelist_id.item_ids
                    global_item = pricelist_items.filtered(lambda x: x.applied_on == '3_global')
                    if global_item:
                        record.coefficient_from_pricelist = global_item[0].coefficient
                        record.price_discount_supplierinfo = global_item[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = global_item[0].base

