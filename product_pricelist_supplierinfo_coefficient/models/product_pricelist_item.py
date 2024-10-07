# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    coefficient = fields.Float(string='Coefficient', default=0.0)

    def _compute_price(self, product, quantity, uom, date, currency):
        result = super()._compute_price(product, quantity, uom, date, currency=currency)

        # Precio sin descuento
        price_without_discount = product.sudo()._get_supplierinfo_pricelist_price(
            self,
            date=date or self.env.context.get("date"),
            quantity=quantity,
        )

        discount = 0.0
        seller = None 

        # Precio según la fórmula
        if self.compute_price == "formula" and self.base == "supplierinfo":
            seller = product.sudo()._select_seller(
                partner_id=self.env.context.get("force_filter_supplier_id"),
                quantity=quantity,
                date=date,
            )

            if seller:
                # Obtener el precio
                price_discounted = seller._get_supplierinfo_pricelist_price()
                discount = seller.discount or 0.0

                # Aplico descuento si existe
                if discount > 0:
                    price_discounted *= (1 - (discount / 100))
                else:
                    price_discounted = price_without_discount  # Si no hay descuento, usar el precio sin descuento

                # Si el coeficiente es mayor a 0, aplica el coeficiente al precio descontado
                if self.coefficient > 0:
                    result = price_discounted * self.coefficient
                else:
                    # Si el coeficiente es 0, verificamos si hay descuento
                    if discount == 0:
                        # Si el descuento también es 0, devuelve 999999
                        result = 999999
                    else:
                        # Si hay descuento, devuelve el precio sin descuento
                        result = price_without_discount
            else:
                # Si no hay vendedor, simplemente devuelve el precio sin descuento
                result = price_without_discount
        else:
            # Si compute_price no es "formula", devuelve el precio sin descuento por defecto
            result = price_without_discount

        return result

