# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, tools, _

from datetime import datetime

class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    coefficient = fields.Float(string='Coefficient', default=0.0)
    show_coefficient = fields.Boolean("Show Coefficient", default=False)
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
    price_from_pricelist = fields.Float(
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
                    if self.price_min_margin:
                        price = max(price, price + self.price_min_margin)
                    if self.price_max_margin:
                        price = min(price, price + self.price_max_margin)
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
                        if self.price_min_margin:
                            price = max(price, price + self.price_min_margin)
                        if self.price_max_margin:
                            price = min(price, price + self.price_max_margin)
                        result = price

        return result
    
    @api.depends('base_pricelist_id.item_ids.coefficient', 'base_pricelist_id.item_ids.price_discount', 'applied_on', 'categ_id', 'product_tmpl_id', 'product_id')
    def _compute_coeff_and_discount(self):
        for record in self:
            record.coefficient_from_pricelist = 0.0
            record.price_from_pricelist = 0.0
            record.show_coefficient = False

            if record.base == 'pricelist' and record.base_pricelist_id:
                if record.applied_on == '2_product_category':
                    pricelist_items = record.base_pricelist_id.item_ids.filtered(
                        lambda x: x.categ_id == record.categ_id
                    )
                    if pricelist_items:
                        record.coefficient_from_pricelist = pricelist_items[0].coefficient
                        record.price_from_pricelist = pricelist_items[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = pricelist_items[0].base

                elif record.applied_on == '1_product':
                    pricelist_items = record.base_pricelist_id.item_ids.filtered(
                        lambda x: x.product_tmpl_id == record.product_tmpl_id
                    )
                    if pricelist_items:
                        record.coefficient_from_pricelist = pricelist_items[0].coefficient
                        record.price_from_pricelist = pricelist_items[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = pricelist_items[0].base
                        
                elif record.applied_on == '0_product_variant':
                    pricelist_items = record.base_pricelist_id.item_ids.filtered(
                        lambda x: x.product_id == record.product_id
                    )
                    if pricelist_items:
                        record.coefficient_from_pricelist = pricelist_items[0].coefficient
                        record.price_from_pricelist = pricelist_items[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = pricelist_items[0].base

                elif record.applied_on == '3_global':
                    pricelist_items = record.base_pricelist_id.item_ids
                    global_item = pricelist_items.filtered(lambda x: x.applied_on == '3_global')
                    if global_item:
                        record.coefficient_from_pricelist = global_item[0].coefficient
                        record.price_from_pricelist = global_item[0].price_discount
                        record.show_coefficient = True
                        record.base_from_pricelist = global_item[0].base

    @api.depends_context('lang')
    @api.depends('compute_price', 'price_discount', 'price_surcharge', 'base', 'price_round', 'coefficient')
    def _compute_rule_tip(self):
        super(ProductPricelistItem, self)._compute_rule_tip()

        for item in self:
            if item.compute_price == 'formula' and item.base == 'supplierinfo':
                base_selection_vals = {elem[0]: elem[1] for elem in self._fields['base']._description_selection(self.env)}
                discount_factor = (100 - item.price_discount) / 100
                discounted_price = 100 * discount_factor
                if item.price_round:
                    discounted_price = tools.float_round(discounted_price, precision_rounding=item.price_round)
                surcharge = tools.format_amount(item.env, item.price_surcharge, item.currency_id)

                if item.coefficient > 0:
                    # If coefficient > to 0
                    item.rule_tip = _(
                        "%(base)s with a %(coefficient_charge)s coefficient and %(surcharge)s extra fee\n"
                        "Example: %(amount)s * %(coefficient_charge)s + %(price_surcharge)s → %(total_amount)s",
                        base=base_selection_vals[item.base],
                        surcharge=surcharge,
                        amount=tools.format_amount(item.env, 100, item.currency_id),
                        coefficient_charge=item.coefficient,
                        price_surcharge=surcharge,
                        total_amount=tools.format_amount(
                            item.env,
                            (100 * item.coefficient) + item.price_surcharge,
                            item.currency_id
                        )
                    )
                else:
                    # No coefficient
                    item.rule_tip = _(
                        "%(base)s with a %(discount)s %% discount and %(surcharge)s extra fee\n"
                        "Example: %(amount)s * %(discount_charge)s + %(price_surcharge)s → %(total_amount)s",
                        base=base_selection_vals[item.base],
                        discount=item.price_discount,
                        surcharge=surcharge,
                        amount=tools.format_amount(item.env, 100, item.currency_id),
                        discount_charge=discount_factor,
                        price_surcharge=surcharge,
                        total_amount=tools.format_amount(
                            item.env,
                            discounted_price + item.price_surcharge,
                            item.currency_id
                        )
                    )
