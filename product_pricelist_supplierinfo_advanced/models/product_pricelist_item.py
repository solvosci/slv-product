# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, tools

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

        # Price according to the formula
        if self.compute_price == "formula" and self.base == "supplierinfo":

            if isinstance(date, datetime):
                date = date.date()

            if self.no_supplierinfo_min_quantity:
                # No matter which minimum qty, we'll get every seller. We set a
                # number absurdidly high
                quantity = 1e9

            seller = product.sudo().with_context(
                override_min_qty=self.no_supplierinfo_min_quantity
            )._select_seller(
                partner_id=self.filter_supplier_id,
                quantity=quantity,
                date=date,
            )

            if seller:
                # Get seller data
                seller_price = seller.price or 0.0
                seller_discount = seller.discount or 0.0
                seller_extra = seller.extra or 0.0
                seller_price_discounted = seller.price_discounted or 0.0

                # If coefficient is > to 0, applu coefficient to price without discount
                if self.coefficient > 0:
                    price = ((seller_price_discounted + seller_extra) * self.coefficient) + self.price_surcharge
                    if self.price_round:
                        price = tools.float_round(price, precision_rounding=self.price_round)
                    result = price
                else:
                    # If coeffient = 0, verify if there is discount
                    if seller_discount == 0:
                        # If discount = 0, return 999999
                        result = 999999
                    else:
                        # If there is discount, return price without discount
                        price_discount = self.price_discount or 0.0 
                        price = (seller_price + seller_extra) * (1 - (price_discount / 100)) + self.price_surcharge
                        if self.price_round:
                            price = tools.float_round(price, precision_rounding=self.price_round)
                        result = price

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
