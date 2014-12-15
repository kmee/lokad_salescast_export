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

from openerp.osv import fields,osv

class product_product(osv.osv):

    _inherit = "product.product"
    _columns = {
    	'service_level': fields.float('Service Level (%)', help=u"Service Level \
    		expresses the probability of being able to service incoming orders  \
    		(or demand) within a reference period without delay from stock on hand."),                
    }
    
    _defaults = {
        'service_level': 98,
        }
    
    _sql_constraints = [
        ('check_service_level', 'check(service_level >= 0 and service_level <= 100)', 'The Service Level should be between 0% and 100%!')
    ]