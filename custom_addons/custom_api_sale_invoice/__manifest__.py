{
    'name': 'Custom API for Sales and Invoices',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'REST API for creating sales orders and invoices',
    'description': """
        This module provides a REST API endpoint to create sales orders and invoices.
    """,
    'author': 'cartona',
    'depends': ['sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
