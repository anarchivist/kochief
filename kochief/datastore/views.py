# Copyright 2009 Gabriel Sean Farrell
#
# This file is part of Kochief.
# 
# Kochief is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Kochief is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Kochief.  If not, see <http://www.gnu.org/licenses/>.

import django.http as http
import django.template.context as tc
import django.template.loader as tl

import kochief.datastore.models as dm

def resource_view(request, resource_id, format='html'):
    resource = dm.Resource.objects.get(id=resource_id)
    if format == 'html':
        context = tc.RequestContext(request)
        context['graph'] = resource.serialize(format='n3')
        template = tl.get_template('datastore/resource.html')
        return http.HttpResponse(template.render(context))
    elif format == 'dc':
        dc_elements = resource
    elif format == 'xml':
        return http.HttpResponse(resource.serialize(format='xml'), 
                mimetype='application/rdf+xml')
    elif format == 'n3':
        return http.HttpResponse(resource.serialize(format='n3'), 
                mimetype='text/n3')
    elif format == 'nt':
        return http.HttpResponse(resource.serialize(format='nt'), 
                mimetype='text/plain')

