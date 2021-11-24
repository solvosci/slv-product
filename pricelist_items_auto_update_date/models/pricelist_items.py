# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.model_create_multi
    def create(self, vals_list):

        # Refactor code ...
        # Adding elements from the form: In the case that more than one
        # pricelist element is added on the same product and rate in error
        # When importing it works correctly without the need for this code
        items = []
        for values in vals_list:
            items.append({'product_tmpl_id': values['product_tmpl_id'],
                          'pricelist_id': values['pricelist_id']})
        for element in items:
            error = False
            for element2 in items:
                if element['pricelist_id'] == element2['pricelist_id'] and element['product_tmpl_id'] == element2['product_tmpl_id']:
                    if not error:
                        error = True
                    else:
                        raise ValidationError(_("Cannot add more than one pricelist item for the same product at the same time!"))

        for values in vals_list:
            if values.get('date_start'):
                for item in self.pricelist_id.item_ids.search([('pricelist_id', '=', values['pricelist_id']), ('product_tmpl_id', '=', values['product_tmpl_id'])], order='date_start asc'):
                    date_min = self.pricelist_id.item_ids.search([('pricelist_id', '=', values['pricelist_id']), ('product_tmpl_id', '=', values['product_tmpl_id'])], order='date_start asc')[0].date_start
                    date_start = datetime.strptime(values['date_start'], '%Y-%m-%d').date()

                    # New date is manor to the smallest date
                    if date_min > date_start:
                        values['date_end'] = date_min - timedelta(days=1)
                        break
                    # TODO When you enter a date_start with the same date_start as another, overwrite it
                    elif item.date_start == date_start:
                        values['date_end'] = item.date_end
                        break
                    # New date is greater than the date_start and date_end is False
                    elif item.date_start < date_start and item.date_end is False:
                        item.date_end = date_start - timedelta(days=1)
                        break
                    # New date is less than the date_start and date_end is False
                    elif item.date_start > date_start and item.date_end is False:
                        values['date_end'] = item.date_end - timedelta(days=1)
                        break
                    # New date is less than or equal to the date_end
                    elif item.date_end and item.date_end >= date_start:
                        values['date_end'] = item.date_end
                        item.date_end = date_start - timedelta(days=1)
                        break

        return super(ProductPricelistItem, self).create(vals_list)
