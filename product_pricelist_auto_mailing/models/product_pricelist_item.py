# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def write(self, vals):
        if self.env.user.id in self.env.company.user_notifying_price_changes_ids.ids:
            self.pricelist_id.write({'mailable_user_ids': [(4, self.env.user.id)]})
        return super().write(vals)
