# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Modulo Prueba Kaur",
    'summary': "Use python code to define taxes",
    'description': """
A tax defined as python code consists of two snippets of python code which are executed in a local environment containing data such as the unit price, product or partner.

"Applicable Code" defines if the tax is to be applied.

"Python Code" defines the amount of the tax.
        """,
    'category': 'Accounting/Accounting',
    'version': '1.0',
    'depends': ['base'],
    'aplication': True,
    'data': ["front.xml"],
    'license': 'LGPL-3',
}