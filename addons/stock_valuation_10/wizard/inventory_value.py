from odoo import api, fields, models,_
import xlwt
import xlsxwriter
from io import StringIO
from io import BytesIO
import base64, urllib
import cStringIO
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception, content_disposition

class Binary(http.Controller):
 @http.route('/download', type='http', auth="public")
 @serialize_exception
 def download_document(self,model,field,id,filename=None, **kw):
    """ Download link for files stored as binary fields.
    :param str model: name of the model to fetch the binary from
    :param str field: binary field
    :param str id: id of the record from which to fetch the binary
    :param str filename: field holding the file's name, if any
    :returns: :class:`werkzeug.wrappers.Response`
    """
    Model = request.env[model]

    fields = [field]

    res = Model.browse(int(id))

    filecontent = base64.b64decode(res.data or '')

    if not filecontent:

        return request.not_found()

    else:

        if not filename:

            filename = '%s_%s' % (model.replace('.', '_'), id)

        return request.make_response(filecontent,

                       [('Content-Type', 'application/octet-stream'),
                        ('Content-Disposition', content_disposition(filename))])

class InventoryValue(models.TransientModel):
    _name = "inventory.value"
    
    company_id = fields.Many2one('res.company', 'Company')
    warehouse_ids = fields.Many2many('stock.warehouse', 'stock_list_rel', 'ware_id', 'stock_id', 'Warehouses')
    location_id = fields.Many2one('stock.location', 'Select Location')
    from_date = fields.Date('From Date',required=True)
    to_date = fields.Date('To Date',required=True)
    display_sumry = fields.Boolean('Display Only Summary')
    categ_ids = fields.Many2many('product.category','prod_categ','all_cat','cat_id',"Categories")
    name = fields.Char('Name')
    excel_sheet_rel = fields.Binary('Download Excel')
    file_name_rel = fields.Char('Excel File', size=64)
    data = fields.Binary('File')
    
#     @api.multi
#     def generate_report(self):
#         
#         return self.env['report'].get_action('stock_valuation.inventory_value_id') 
    
    @api.multi
    def generate_report(self):
        return self.env['report'].get_action(self,'stock_valuation_10.inventory_value_report_id')
    
    @api.multi
    def getStockWithCategory(self):
        categ_obj = self.env['inventory.value']
        prod_obj = self.env['product.product']
        move_line_obj = self.env['stock.move']
        categ_list =[]
        start_qty = {}
        end_qty = {}
        receive = {}
        sales = {}
        internal = {}
        adjust = {}
        
        if self.categ_ids:
            query_start = "SELECT t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id"%(self.from_date + ' 00:00:00', self.from_date + ' 23:59:59')
            print("=====query_start====",query_start)
            self.env.cr.execute(query_start)
            start_stock_results = self.env.cr.dictfetchall()
            print("start_stock_resultsstart_stock_results",start_stock_results)
            for rec in start_stock_results:
                print("recrecrecrecrecrecrecrec",rec)
                start_qty.update({rec.get('categ_id'): rec.get('sum')})
                
            query_end = "SELECT t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id"%(self.to_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_end)
            end_stock_result = self.env.cr.dictfetchall()
            for rec in end_stock_result:
                end_qty.update({rec.get('categ_id'): rec.get('sum')})
                
            query_recv = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'supplier') and s.location_dest_id in (select id from stock_location where usage = 'internal')GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_recv)
            recv_stock_result = self.env.cr.dictfetchall()
            for rece in recv_stock_result:
                receive.update({rece.get('product_id'): rece.get('sum')})
                print("receivereceivereceivereceive-----------------------------",receive)
                  
            query_sale = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'customer') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_sale)
            sale_stock_result = self.env.cr.dictfetchall()
            for sale in sale_stock_result:
                sales.update({sale.get('product_id'): sale.get('sum')})
                print("salessalessalessales-----------------------------",sales)
            
            query_int = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' AND s.picking_type_id in (select id from stock_picking_type where code = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'internal') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_int)
            int_stock_result = self.env.cr.dictfetchall()
            print("int_stock_resultint_stock_result-----------------------------",int_stock_result)
            for intrn in int_stock_result:
                internal.update({intrn.get('product_id'): intrn.get('sum')})
                print("internal-----------------------------",internal)
               
            query_adjust = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' and s.location_dest_id in (select id from stock_location where usage = 'inventory') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_adjust)
            adjust_stock_result = self.env.cr.dictfetchall()
            print("adjust_stock_resultadjust_stock_result-----------------------------",adjust_stock_result)
            for adj in adjust_stock_result:
                adjust.update({adj.get('product_id'): adj.get('sum')})
                print("adjust_adddddddddddddddddddddd-----------",adjust)
           
            result_list = []
            product_ids = self.env['product.product'].search([])
            for prod in product_ids:
                for each in self.categ_ids:
                    if prod.categ_id == each:
                        total = end_qty.get(prod.id,0.0) * prod.standard_price
                        result_list.append({
                            'name': prod.categ_id.name,
                            'start_qty': start_qty.get(prod.id,0.0),
                            'end_qty': end_qty.get(prod.id,0.0),
                            'receive':receive.get(prod.id,0.0),
                            'sales':sales.get(prod.id,0.0),
                            'internal': internal.get(prod.id,0.0),
                            'adjust':adjust.get(prod.id,0.0),
                            'cost': prod.standard_price,
                            'total_value': total
                        })
            print("result_listresult_list-----------------------------",result_list)
        else:
            result_list = []
            query_start = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.from_date + ' 23:59:59')
            print("=====query_startellllllllssssssssss====",query_start)
            self.env.cr.execute(query_start)
            start_stock_results = self.env.cr.dictfetchall()
            print("start_stock_resultsstart_stock_results",start_stock_results)
            for rec in start_stock_results:
                print("recrecrecrecrecrecrecrec",rec)
                start_qty.update({rec.get('product_id'): rec.get('sum')})
                
            query_end = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id,s.product_id"%(self.to_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_end)
            end_stock_result = self.env.cr.dictfetchall()
            for end in end_stock_result:
                end_qty.update({end.get('product_id'): end.get('sum')})
                
            query_recv = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'supplier') and s.location_dest_id in (select id from stock_location where usage = 'internal')GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_recv)
            recv_stock_result = self.env.cr.dictfetchall()
            for rece in recv_stock_result:
                receive.update({rece.get('product_id'): rece.get('sum')})
                print("receivereceivereceivereceive-----------------------------",receive)
                  
            query_sale = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'customer') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_sale)
            sale_stock_result = self.env.cr.dictfetchall()
            for sale in sale_stock_result:
                sales.update({sale.get('product_id'): sale.get('sum')})
                print("salessalessalessales-----------------------------",sales)
                
            query_int = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' AND s.picking_type_id in (select id from stock_picking_type where code = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'internal') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_int)
            int_stock_result = self.env.cr.dictfetchall()
            print("int_stock_resultint_stock_result-----------------------------",int_stock_result)
            for intrn in int_stock_result:
                internal.update({intrn.get('product_id'): intrn.get('sum')})
                print("internal-----------------------------",internal)
           
            query_adjust = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' and s.location_dest_id in (select id from stock_location where usage = 'inventory') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_adjust)
            adjust_stock_result = self.env.cr.dictfetchall()
            print("adjust_stock_resultadjust_stock_result-----------------------------",adjust_stock_result)
            for adj in adjust_stock_result:
                adjust.update({adj.get('product_id'): adj.get('sum')})
                print("adjust_adddddddddddddddddddddd-----------",adjust)
            product_ids = self.env['product.product'].search([])
            for prod in product_ids:
                total = end_qty.get(prod.id,0.0) *  prod.standard_price
                result_list.append({
                    'name':prod.categ_id.name,
                    'start_qty': start_qty.get(prod.id,0.0),
                    'end_qty': end_qty.get(prod.id,0.0),
                    'receive':receive.get(prod.id,0.0),
                    'sales':sales.get(prod.id,0.0),
                    'internal': internal.get(prod.id,0.0),
                    'adjust':adjust.get(prod.id,0.0),
                    'cost': prod.standard_price,
                    'total_value': total
                })
            print("result_listresult_listelllllllllsssssssssss-----------------------------",result_list)
        
        return result_list
   
    @api.multi
    def getcategory(self):
        categ_obj = self.env['inventory.value']
        prod_obj = self.env['product.product']
        move_line_obj = self.env['stock.move']
        categ_list =[]
        start_qty = {}
        end_qty = {}
        receive = {}
        sales = {}
        internal = {}
        adjust = {}
        
        if self.categ_ids:
            query_start = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.from_date + ' 23:59:59')
            print("=====query_start====",query_start)
            self.env.cr.execute(query_start)
            start_stock_results = self.env.cr.dictfetchall()
            print("start_stock_resultsstart_stock_results",start_stock_results)
            for rec in start_stock_results:
                print("recrecrecrecrecrecrecrec",rec)
                start_qty.update({rec.get('product_id'): rec.get('sum')})
                
            query_end = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id,s.product_id"%(self.to_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_end)
            end_stock_result = self.env.cr.dictfetchall()
            for end in end_stock_result:
                end_qty.update({end.get('product_id'): end.get('sum')})
                
            query_recv = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'supplier') and s.location_dest_id in (select id from stock_location where usage = 'internal')GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_recv)
            recv_stock_result = self.env.cr.dictfetchall()
            for rece in recv_stock_result:
                receive.update({rece.get('product_id'): rece.get('sum')})
                print("receivereceivereceivereceive-----------------------------",receive)
                  
            query_sale = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'customer') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_sale)
            sale_stock_result = self.env.cr.dictfetchall()
            for sale in sale_stock_result:
                sales.update({sale.get('product_id'): sale.get('sum')})
                print("salessalessalessales-----------------------------",sales)
                
            query_int = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' AND s.picking_type_id in (select id from stock_picking_type where code = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'internal') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_int)
            int_stock_result = self.env.cr.dictfetchall()
            print("int_stock_resultint_stock_result-----------------------------",int_stock_result)
            for intrn in int_stock_result:
                internal.update({intrn.get('product_id'): intrn.get('sum')})
                print("internal-----------------------------",internal)
           
            query_adjust = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' and s.location_dest_id in (select id from stock_location where usage = 'inventory') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_adjust)
            adjust_stock_result = self.env.cr.dictfetchall()
            print("adjust_stock_resultadjust_stock_result-----------------------------",adjust_stock_result)
            for adj in adjust_stock_result:
                adjust.update({adj.get('product_id'): adj.get('sum')})
                print("adjust_adddddddddddddddddddddd-----------",adjust)
           
            result_list = []
            product_ids = self.env['product.product'].search([])
            for prod in product_ids:
                for each in self.categ_ids:
                    if prod.categ_id == each:
                        total = end_qty.get(prod.id,0.0) * prod.standard_price
                        result_list.append({
                            'categ_name': prod.categ_id.name,
                            'name': prod.name,
                            'start_qty': start_qty.get(prod.id,0.0),
                            'end_qty': end_qty.get(prod.id,0.0),
                            'receive':receive.get(prod.id,0.0),
                            'sales':sales.get(prod.id,0.0),
                            'internal': internal.get(prod.id,0.0),
                            'adjust':adjust.get(prod.id,0.0),
                            'cost': prod.standard_price,
                            'total_value': total
                        })
                    
            print("result_listresult_list-----------------------------",result_list)
        else:
            result_list = []
            query_start = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.from_date + ' 23:59:59')
            print("=====query_startellllllllssssssssss====",query_start)
            self.env.cr.execute(query_start)
            start_stock_results = self.env.cr.dictfetchall()
            print("start_stock_resultsstart_stock_results",start_stock_results)
            for rec in start_stock_results:
                print("recrecrecrecrecrecrecrec",rec)
                start_qty.update({rec.get('product_id'): rec.get('sum')})
                
            query_end = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' GROUP BY t.categ_id,s.product_id"%(self.to_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_end)
            end_stock_result = self.env.cr.dictfetchall()
            for end in end_stock_result:
                end_qty.update({end.get('product_id'): end.get('sum')})
                
            query_recv = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'supplier') and s.location_dest_id in (select id from stock_location where usage = 'internal')GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_recv)
            recv_stock_result = self.env.cr.dictfetchall()
            for rece in recv_stock_result:
                receive.update({rece.get('product_id'): rece.get('sum')})
                print("receivereceivereceivereceive-----------------------------",receive)
                  
            query_sale = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done'and s.location_id in (select id from stock_location where usage = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'customer') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_sale)
            sale_stock_result = self.env.cr.dictfetchall()
            for sale in sale_stock_result:
                sales.update({sale.get('product_id'): sale.get('sum')})
                print("salessalessalessales-----------------------------",sales)
                
            query_int = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' AND s.picking_type_id in (select id from stock_picking_type where code = 'internal') and s.location_dest_id in (select id from stock_location where usage = 'internal') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_int)
            int_stock_result = self.env.cr.dictfetchall()
            print("int_stock_resultint_stock_result-----------------------------",int_stock_result)
            for intrn in int_stock_result:
                internal.update({intrn.get('product_id'): intrn.get('sum')})
                print("internal-----------------------------",internal)
           
            query_adjust = "SELECT s.product_id,t.categ_id,sum(s.product_uom_qty) FROM stock_move s, product_product p, product_template t  WHERE s.product_id = p.id and t.id= p.product_tmpl_id and s.date >= '%s' and s.date <= '%s' AND s.state = 'done' and s.location_dest_id in (select id from stock_location where usage = 'inventory') GROUP BY t.categ_id,s.product_id"%(self.from_date + ' 00:00:00', self.to_date + ' 23:59:59')
            self.env.cr.execute(query_adjust)
            adjust_stock_result = self.env.cr.dictfetchall()
            print("adjust_stock_resultadjust_stock_result-----------------------------",adjust_stock_result)
            for adj in adjust_stock_result:
                adjust.update({adj.get('product_id'): adj.get('sum')})
                print("adjust_adddddddddddddddddddddd-----------",adjust)
            product_ids = self.env['product.product'].search([])
            for prod in product_ids:
                total = end_qty.get(prod.id,0.0) *  prod.standard_price
                result_list.append({
                    'categ_name': prod.categ_id.name,
                    'name': prod.name,
                    'start_qty': start_qty.get(prod.id,0.0),
                    'end_qty': end_qty.get(prod.id,0.0),
                    'receive':receive.get(prod.id,0.0),
                    'sales':sales.get(prod.id,0.0),
                    'internal': internal.get(prod.id,0.0),
                    'adjust':adjust.get(prod.id,0.0),
                    'cost': prod.standard_price,
                    'total_value': total
                })
            print("result_listresult_listelllllllllsssssssssss-----------------------------",result_list)
        return result_list
  
    
    @api.multi
    def getmulticompany(self):
        comp_obj = self.env['res.company']
        ware_obj = self.env['stock.warehouse']
        comp_ids = comp_obj.search([])
        comp_list =[]
        ware_list =[]
        total = []
        for comp in comp_ids:
            comp_list.append(comp)
            ware_ids = ware_obj.search([('company_id','=',comp.id)])
            w_name = ''
            for ware in ware_ids:
                if w_name :
                    w_name = w_name +', '+ ware.name
                else:
                    w_name = ware.name
            print("================warewarewarewarename",w_name)
            ware_list.append(w_name)
        print("================comp_listcomp_listcomp_list",comp_list)
        print("================ware_listware_listware_listware_list",ware_list)
        total.append(comp_list)
        total.append(ware_list)
        return total


        
    @api.multi
    def print_xls_report(self):
        """ Generate xls sheet of trail balance report """
        print ("self====",self)
        
        data = self.read()[0]
        print ("data========",data)
        fp = BytesIO()
        # workbook = xls.Workbook("/var/www/html/valuation.xls")
        workbook = xlwt.Workbook()
        header_format1 = xlwt.XFStyle()

        borders1 = xlwt.Borders()
        borders1.left = 2
        borders1.right = 2
        borders1.top = 2
        borders1.bottom = 2

        header_format1.borders = borders1
        header_format1.bold = 1
        header_format1.align = 'center'
        header_format1.valign = 'vcenter'
        header_format1.bg_color = 'silver'
        header_format1.text_wrap = 1
        header_format1.font_name = 'Verdana'
        header_format1.font_size = 12

        header_format2 = xlwt.XFStyle()
        header_format2.borders = borders1
        header_format2.bold = 1
        header_format2.align = 'center'
        header_format2.valign = 'vcenter'
        header_format2.bg_color = 'silver'
        header_format2.text_wrap = 1
        header_format2.font_name = 'Verdana'
        header_format2.font_size = 11

        normal_format1 = xlwt.XFStyle()
        normal_format1.align = 'center'
        normal_format1.valign = 'vcenter'
        normal_format1.font_name = 'Calibri'
        normal_format1.text_wrap = 1
        normal_format1.font_size = 11

        normal_format2 = xlwt.XFStyle()
        normal_format2.align = 'right'
        normal_format2.valign = 'vcenter'
        normal_format2.font_name = 'Calibri'
        normal_format2.bg_color = 'silver'
        normal_format2.text_wrap = 1
        normal_format2.font_size = 11

        header_value1 = xlwt.XFStyle()
        header_value1.valign = 'vcenter'
        header_value1.font_name = 'Calibri'
        header_value1.bg_color = 'silver'
        header_value1.text_wrap = 1
        header_value1.font_size = 11

       
        file_name = 'inventory_value.xlsx'
        report_name = 'Inventory Valuation Report'
        worksheet = workbook.add_sheet(report_name)
        print ("worksheetworksheet========",worksheet)
        
        worksheet.write_merge(1,3,0,10, self.company_id.name,header_format2)
        
        worksheet.write_merge(4,4,0,2, 'Date',header_format1)
        worksheet.write_merge(4,4,3,4, 'Company',header_format1)
        worksheet.write_merge(4,4,5,6, 'Warehouse',header_format1)
        worksheet.write_merge(4,4,7,8, 'Currency',header_format1)
        worksheet.write_merge(4,4,9,10, 'Display',header_format1)
        
        worksheet.write_merge(5,5,0,2,self.from_date+' To '+self.to_date,normal_format1)
        worksheet.write_merge(5,5,3,4, self.company_id.name,header_value1)
        worksheet.write_merge(5,5,5,6, self.warehouse_ids.name,header_value1)
        worksheet.write_merge(5,5,7,8, self.company_id.currency_id.name,header_value1)
        if self.display_sumry == False :
            worksheet.write_merge(5,5,9,10,'Display Report',header_value1)
        else:
            worksheet.write_merge(5,5,9,10,'Summary Report',header_value1)
       
       # set Column width size
        worksheet.col(0).width = 2000
        worksheet.col(1).width = 2000
        worksheet.col(2).width = 2000
        worksheet.col(3).width = 2000
        worksheet.col(4).width = 2000
        worksheet.col(5).width = 2000
        worksheet.col(6).width = 2000
        worksheet.col(7).width = 2000
        worksheet.col(8).width = 2000
        worksheet.col(9).width = 2000
        # worksheet.set_column('A:A', 20)
        # worksheet.set_column('B:B', 25)
        # worksheet.set_column('C:C', 12)
        # worksheet.set_column('D:D', 12)
        # worksheet.set_column('E:E', 12)
        # worksheet.set_column('F:F', 12)
        # worksheet.set_column('G:G', 12)
        # worksheet.set_column('H:H', 12)
        # worksheet.set_column('I:I', 12)
        # worksheet.set_column('J:J', 12)
       # Add Company Name and date
        company_name_header = 'Senex Garment Accessories Limited'+'\n'+'Trial Balance Sheet'
        date_string = ''
        
       
        if self.display_sumry == False :
            data = self.getcategory()
            print (data)
            
    #         worksheet.write('A7', 'Category Name',header_format2)
    #         worksheet.write('B7', 'Product Name',header_format2)
    # #         worksheet.write('J1', 'Product Barcode')
    #         worksheet.write('C7', 'Beginning',header_format2)
    #         worksheet.write('D7', 'Received',header_format2)
    #         worksheet.write('E7', 'Sale',header_format2)
    #         worksheet.write('F7', 'Internal',header_format2)
    #         worksheet.write('G7', 'Adjustments',header_format2)
    #         worksheet.write('H7', 'Ending',header_format2)
    #         worksheet.write('I7', 'Cost',header_format2)
    #         worksheet.write('J7', 'Total Value',header_format2)
    #         worksheet.write('J1', 'Hello world')
            
            count = 8
            total_start_qty = 0
            total_receive = 0
            total_sales = 0
            total_internal = 0
            total_adjust = 0
            total_end_qty = 0
            grand_total = 0
            row = 0
            for rec in data:
                total_start_qty+=rec.get('start_qty')
                total_receive+= rec.get('receive')
                total_sales+= rec.get('sales')
                total_internal+= rec.get('internal')
                total_adjust+= rec.get('adjust')
                total_end_qty+= rec.get('end_qty')
                grand_total += rec.get('total_value')
                worksheet.write(count, 0, rec.get('categ_name'),normal_format1)
                worksheet.write(count, 1, rec.get('name'),normal_format1)
                worksheet.write(count, 2, rec.get('start_qty'),normal_format2)
                worksheet.write(count, 3, rec.get('receive'),normal_format2)
                worksheet.write(count, 4, rec.get('sales'),normal_format2)
                worksheet.write(count, 5, rec.get('internal'),normal_format2)
                worksheet.write(count, 6, rec.get('adjust'),normal_format2)
                worksheet.write(count, 7, rec.get('end_qty'),normal_format2)
                worksheet.write(count, 8, rec.get('cost'),normal_format2)
                worksheet.write(count, 9, rec.get('total_value'),normal_format2)
                count+=1
            worksheet.write(count, 0, "Total Inventory",header_format2)
            worksheet.write(count, 1, total_start_qty,normal_format2)
            worksheet.write(count, 3, total_receive,normal_format2)
            worksheet.write(count, 4, total_sales,normal_format2)
            worksheet.write(count, 5, total_internal,normal_format2)
            worksheet.write(count, 6, total_adjust,normal_format2)
            worksheet.write(count, 7, total_end_qty,normal_format2)
            worksheet.write(count, 8, '-',normal_format2)
            worksheet.write(count, 9, grand_total,normal_format2)
        else:
            data = self.getStockWithCategory()
            print (data)
    #         worksheet.write('A1', 'Category Name')
            worksheet.write(7,0, 'Product Name',header_format2)
    #         worksheet.write('J1', 'Product Barcode')
            worksheet.write(7,1, 'Beginning',header_format2)
            worksheet.write(7,2, 'Received',header_format2)
            worksheet.write(7,3, 'Sale',header_format2)
            worksheet.write(7,4, 'Internal',header_format2)
            worksheet.write(7,5, 'Adjustments',header_format2)
            worksheet.write(7,6, 'Ending',header_format2)
#             worksheet.write('H7', 'Cost')
            worksheet.write(7,7, 'Total Value',header_format2)
    #         worksheet.write('J1', 'Hello world')
            
            count = 8
            total_start_qty = 0
            total_receive = 0
            total_sales = 0
            total_internal = 0
            total_adjust = 0
            total_end_qty = 0
            grand_total = 0
            for rec in data:
                total_start_qty+=rec.get('start_qty')
                total_receive+= rec.get('receive')
                total_sales+= rec.get('sales')
                total_internal+= rec.get('internal')
                total_adjust+= rec.get('adjust')
                total_end_qty+= rec.get('end_qty')
                grand_total += rec.get('total_value')
                worksheet.write(count,0, rec.get('name'),normal_format1)
                worksheet.write(count,1, rec.get('start_qty'),normal_format2)
                worksheet.write(count,2, rec.get('receive'),normal_format2)
                worksheet.write(count, 3,rec.get('sales'),normal_format2)
                worksheet.write(count,4,rec.get('internal'),normal_format2)
                worksheet.write(count,5, rec.get('adjust'),normal_format2)
                worksheet.write(count,6,rec.get('end_qty'),normal_format2)
#                 worksheet.write('H'+ count, rec.get('cost'))
                worksheet.write(count,8, rec.get('total_value'),normal_format2)
                count+=1
            worksheet.write(count, 0, "Total Inventory",header_format2)
            worksheet.write(count, 1, total_start_qty,normal_format2)
            worksheet.write(count, 2, total_receive,normal_format2)
            worksheet.write(count, 3, total_sales,normal_format2)
            worksheet.write(count, 4, total_internal,normal_format2)
            worksheet.write(count, 5, total_adjust,normal_format2)
            worksheet.write(count, 6, total_end_qty,normal_format2)
#                 worksheet.write('H'+ count, rec.get('cost'))
            worksheet.write(count, 7, grand_total,normal_format2)
            
        stream = cStringIO.StringIO()
        workbook.save(stream)
        out=base64.encodestring(stream.getvalue())
        self.write({'data': out})
        print "===outout====>",out
        return {
            'type' : 'ir.actions.act_url',
            'url': '/download?model=inventory.value&field=data&id=%s&filename=valuation.xls'%(self.id),
            'target': 'new',
        }
        
    
