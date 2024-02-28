# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.product_template_websale_search_extended.controllers.main import WebsiteSaleSearch


class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        domain = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
        domain = WebsiteSaleSearch._add_search_domain(domain, search, 'partner_ref')
        domain = WebsiteSaleSearch._add_search_domain(domain, search, 'barcode')
        return domain
