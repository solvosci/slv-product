# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    'name': 'Product Pricelist Auto Mailing',
    'summary': '''
        Adds automatic notification when certain users modify a pricelist
    ''',
    'author': 'Solvos',
    'license': 'LGPL-3',
    'version': '13.0.1.0.1',
    'category': 'Product',
    'website': 'https://github.com/solvosci/slv-product',
    'depends': ['product'],
    'data': [
        'data/mail_template_data.xml',
        'views/res_config_settings_view.xml',
        'views/product_pricelist_view.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
}
