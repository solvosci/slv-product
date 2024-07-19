# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, _, fields


class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']

    mailable_user_ids = fields.Many2many('res.users', readonly=True, copy=False)

    def send_mail(self, mailable_pricelist_ids):
        body = []
        ctx = self.env.context.copy()
        for pricelist in mailable_pricelist_ids:
            body.append(_('The pricelist %s, has been changed by the following users: %s') % (pricelist.name, ' ,'.join(pricelist.mailable_user_ids.mapped('name'))))
            pricelist.mailable_user_ids = False
        ctx.update({'body': body})
        pricelist_template_id = self.env.ref('product_pricelist_auto_mailing.mail_template_data_pricelist_notification')
        return pricelist_template_id.with_context(ctx).send_mail(mailable_pricelist_ids[0].id, force_send=True)

    def send_notification(self):
        mailable_pricelist_ids = self.env['product.pricelist'].search([('mailable_user_ids', '!=', False)])
        if mailable_pricelist_ids:
            ctx = self.env.context.copy()
            ctx.update({'lang': mailable_pricelist_ids[0].company_id.partner_id.lang})
            return self.with_context(ctx).send_mail(mailable_pricelist_ids)
        return False
