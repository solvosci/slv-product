# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        params = super()._loader_params_product_product()
        params["search_params"]["fields"].append("list_price_2")
        return params

    # def _process_pos_ui_product_product(self, products):
    #     super()._process_pos_ui_product_product(products)
    #     # According to https://github.com/odoo/odoo/blob/bfd70fe337e52c1f132f9cae526ed5faf5b577a8/addons/point_of_sale/static/src/app/store/models.js#L326
    #     # "lst_price" is used
    #     # lst_price is defined here (based on list_price): https://github.com/odoo/odoo/blob/f8a64c973bbfed5074c5306e88d9143ebca63cc6/addons/product/models/product_product.py#L273
    #     # and loaded by POS session here: https://github.com/odoo/odoo/blob/bfd70fe337e52c1f132f9cae526ed5faf5b577a8/addons/point_of_sale/models/pos_session.py#L2064
    #     # Then, replacing here lst_price should be enough
    #     # for product in products:
    #     #     product['list_price_2'] = self.env['product.product'].browse(product['id']).list_price_2
