# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo all import for Sales, Purchase, Invoice, Inventory,BOM,Customer/Supplier Payment, Bank Statement, Journal Entry, Picking, Product, Customer.',
    'version': '10.0.1.8',
    'sequence': 4,
    'summary': 'Easy to import all odoo data i.e Invoice, Sale, Inventory, Purchase, Picking, Product and Customer.',
    'price': 89,
    'currency': 'EUR',
    'category' : 'Extra Tools',
    'description': """

	BrowseInfo developed a new odoo/OpenERP module apps 
	This module use for following easy import.
	Import Stock from CSV and Excel file.
    Import Stock inventory from CSV and Excel file.
	Import inventory adjustment, import stock balance
	Import opening stock balance from CSV and Excel file.
	Import Sale order, Import sales order, Import Purchase order, Import purchases.
	Import sale order line, import purchase order line, Import data, Import files, Import data from third party software
	Import invoice from CSV, Import Bulk invoices easily.Import warehouse data,Import warehouse stock.Import product stock.
	Invoice import from CSV, Invoice line import from CSV, Sale import, purchase import
	Inventory import from CSV, stock import from CSV, Inventory adjustment import, Opening stock import. 
	Import product from CSV, Import customer from CSV, Product Import,Customer import, Odoo CSV bridge,Import CSV brige on Odoo.Import csv data on odoo.All import, easy import, Import odoo data, Import CSV files, Import excel files 
	Import tools Odoo, Import reports, import accounting data, import sales data, import purchase data, import data in odoo, import record, Import inventory.import data on odoo,Import data from Excel, Import data from CSV.Odoo Import Data
    """,
    'author': 'BrowseInfo',
    'website': '',
    'live_test_url':'https://www.youtube.com/watch?v=bG7ImzFkSfo',
    'depends': ['base', 'sale', 'account', 'account_accountant', 'purchase', 'stock','mrp'],
    'data': [
             "views/account_invoice.xml",
             "views/purchase_invoice.xml",
             "views/sale.xml",
             "views/stock_view.xml",
             "views/product_view.xml",
             "views/partner.xml",
             "views/picking_view.xml",
             "views/customer_payment.xml",
             "views/import_order_lines_view.xml",
             "views/import_po_lines_view.xml",
             "views/import_invoice_lines_view.xml",
             "views/bank_statement.xml",
             "views/account_move.xml",
             "views/supp_info.xml",
             "views/mrp.xml",
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images':['static/description/Banner.png'],



}
