{
	"name": "Stock Card", 
# 	"version": "1.0", 
# 	'price': 49.99,
	'currency': 'USD',
	"depends": [
		"stock"
	], 
	"author": "akhmad.daniel@gmail.com", 
	"category": "Warehouse", 
	"description": """\

Manage
======================================================================

* this modul to display stock card per item per Warehouse


""",
	"data": [
		"menu.xml", 
		"view/stock_card.xml", 
		"view/stock_summary.xml",
		"report/stock_card.xml",
		"data/ir_sequence.xml",
		"security/ir.model.access.csv",
	],
	"installable": True,
	"auto_install": False,
}
