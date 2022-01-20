# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Product Security via Inventory - Main module",
    "summary": """
        Adds new security group for product management
        based on Inventory hierarchy
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/solvosci/slv-product",
    "depends": ["stock", "purchase", "sale"],
    "data": [
        "security/product_security_main_security.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
}
