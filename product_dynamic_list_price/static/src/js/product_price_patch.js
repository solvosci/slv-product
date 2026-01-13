/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Product } from "@point_of_sale/app/store/models";

patch(Product.prototype, {
    get_price(pricelist, quantity, price_extra = 0, recurring = false) {
        const price = super.get_price(
            pricelist,
            quantity,
            price_extra,
            recurring
        );

        if (this.list_price_2) {
            return this.list_price_2;
        }

        return price;
    },
});
