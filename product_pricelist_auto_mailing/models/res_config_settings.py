# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    user_notified_for_price_changes_ids = fields.Many2many(
        related='company_id.user_notified_for_price_changes_ids',
        readonly=False,
    )
    user_notifying_price_changes_ids = fields.Many2many(
        related='company_id.user_notifying_price_changes_ids',
        readonly=False,
    )

class ResCompany(models.Model):
    _inherit = 'res.company'

    user_notified_for_price_changes_ids = fields.Many2many(
        'res.users',
        'user_notified_pricelist',
        readonly=False
    )
    user_notifying_price_changes_ids = fields.Many2many(
        'res.users',
        'user_notifying_pricelist',
        readonly=False,
    )
