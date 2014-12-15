# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2014  KMEE  - www.kmee.com.br - Luis Felipe Mileo             #
# Copyright (C) 2014  KMEE  - www.kmee.com.br - Matheus Felix                 #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU General Public License for more details.                                 #
#                                                                             #
#You should have received a copy of the GNU General Public License            #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

import csv
import base64
from io import StringIO, BytesIO
from openerp.osv import orm, fields
from openerp.tools.translate import _

class KmeeLokadExportTsv(orm.TransientModel):
    """ Exportar Lokad TSV File"""
    _name = 'kmee_lokad.export_tsv'
    _description = 'Export Lokad TSV File'
    _columns = {
        'item_name': fields.char('Name', size=255),
        'order_name': fields.char('Name', size=255),
        'start_date': fields.date('Initial date:'),
        'final_date':  fields.date('Final date:'),
        'file_itens': fields.binary('Lokad Itens', readonly=True),
        'file_order': fields.binary('Lokad Order', readonly=True),
        'state': fields.selection(
                [('init', 'init'), ('done', 'done')], 'state', readonly=True),
                }
    
    _defaults = {
                'state': 'init',
                }
    
    def _get_product_ids(self, cr, uid, ids, data, context=None):
        if not context:
            context = {}
        return context.get('active_ids', [])

    def _export_order(self, cr, uid, ids, data, context):
     
        active_ids = self._get_product_ids(cr, uid, ids, data, context)
        
        cr.execute("""  SELECT al.product_id, i.date_invoice, sum(al.quantity) \
                        FROM account_invoice i \
                        JOIN account_invoice_line al \
                        ON i.id = al.invoice_id \
                        WHERE i.date_invoice between (%s) \
                        AND (%s) AND i.type='out_invoice' AND i.state='open' or i.state='paid' \
                        group by al.product_id, i.date_invoice ORDER BY al.product_id""", (data['start_date'],data['final_date'],))
        res = cr.fetchall()
        
        head = ['ID', 'OrderDate','Quantity']
        
        orderFile = BytesIO()
        
        with orderFile as tsvfile:
            spamwriter = csv.writer(tsvfile, delimiter='\t',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(head)
            for line in res:   
                while (line[0] in active_ids):             
                    spamwriter.writerow(list(line))
                    break
            return orderFile.getvalue()


    def _export_item(self, cr, uid, ids, data, context):
        
        prod_obj = self.pool.get('product.product')
        active_ids = self._get_product_ids(cr, uid, ids, data, context)
        
        head = ['Id','LabelName','TagLabelCategory','TagSubcategory',
                        'ServiceLevel','LeadTime','StockOnHand','StockOnOrder','LotMultiplier']
        
        itemFile = BytesIO()
        
        with itemFile as tsvfile:
            spamwriter = csv.writer(tsvfile, delimiter='\t',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(head)
            for prod in prod_obj.browse(cr, uid, active_ids, context):
                delay = min_qty = 0
                for seller in prod.seller_ids:
                    delay = seller.delay 
                    min_qty = seller.min_qty
                    break
                product = [prod.id, prod.name.encode('utf8'), prod.categ_id.parent_id.id, prod.categ_id.id,
                           prod.service_level, delay, prod.qty_available,
                           prod.incoming_qty, min_qty or 0]
                spamwriter.writerow(product)
                   
            return itemFile.getvalue()

   
    def export(self, cr, uid, ids, context=False):
        
        data = self.read(cr, uid, ids, [], context=context)[0]
        
        orderFile = self._export_order(cr, uid, ids, data, context)        
        itemFile = self._export_item(cr, uid, ids, data, context)
        
        self.write(cr, uid, ids, {'state': 'done', 'file_order': base64.b64encode(orderFile), 'order_name': "lokad_order.tsv",
                                  'file_itens': base64.b64encode(itemFile), 'item_name': "lokad_item.tsv"},
                    context=context)
        
        mod_obj = self.pool.get('ir.model.data')
        model_data_ids = mod_obj.search(
            cr, uid, [('model', '=', 'ir.ui.view'),
            ('name', '=', 'kmee_lokad_export_tsv_form')],
            context=context)
        resource_id = mod_obj.read(
            cr, uid, model_data_ids,
            fields=['res_id'], context=context)[0]['res_id']

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': data['id'],
            'views': [(resource_id, 'form')],
            'target': 'new',
        }
