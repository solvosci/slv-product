# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleSearch():

    def _add_search_domain(domain, search, field):
        domain.insert(2, '|')
        domain += [(field, 'ilike', search)]
        return domain
