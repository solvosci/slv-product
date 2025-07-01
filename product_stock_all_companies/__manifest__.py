# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Product Stock All Companies",
    "summary": """
        Show the stock of a product in all the warehouses, even if they are from other companies
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Inventory/Inventory",
    "website": "https://github.com/solvosci/slv-product",
    "depends": ["product","stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
    ],
    'installable': True,
}
