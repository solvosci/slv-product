# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, _, fields, Command


class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']

    mailable_user_ids = fields.Many2many('res.users', copy=False)

    def send_notification(self):
        mailable_pricelist_ids = self.env['product.pricelist'].search([('mailable_user_ids', '!=', False)])
        user_notified_for_price_changes_ids = self.env.company.user_notified_for_price_changes_ids.partner_id
        if mailable_pricelist_ids and user_notified_for_price_changes_ids:
            body = []
            for pricelist in mailable_pricelist_ids:
                body.append(_('The pricelist %s, has changed for users: %s') % (pricelist.name, ' ,'.join(pricelist.mailable_user_ids.mapped('name'))))
                pricelist.mailable_user_ids = False
            ctx = self.env.context.copy()
            ctx.update({'body': body})
            pricelist_template_id = self.env.ref('product_pricelist_auto_mailing.mail_template_data_pricelist_notification')
            return pricelist_template_id.with_context(ctx).send_mail(
                mailable_pricelist_ids[0].id,
                email_values={
                    "recipient_ids": [Command.set(user_notified_for_price_changes_ids.ids)],
                },
                force_send=True,
            )
