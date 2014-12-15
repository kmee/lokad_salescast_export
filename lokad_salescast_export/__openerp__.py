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


{
    'name': 'Lokad SalesCast Export',
    'version': '0.1',
    'category': 'Warehouse',
    'description': """""",
    'author': 'KMEE',
    'license': 'AGPL-3',
    'website': 'http://www.kmee.com.br',
    'depends': [
        'stock',
    ],
    'data': [
	'product_view.xml',
	'wizard/lokad_export.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}
