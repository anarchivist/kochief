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

from django.http import HttpResponse, Http404
from django.template import loader, RequestContext

from kochief.datastore import models

def resource_view(request, id='', format='html'):
    resource = models.get_resource(id)
    if format == 'html':
        context = RequestContext(request)
        context['graph'] = resource.serialize(format='n3')
        template = loader.get_template('datastore/resource.html')
        return HttpResponse(template.render(context))
    elif format == 'xml':
        return HttpResponse(resource.serialize(), 
                mimetype='application/rdf+xml')
    elif format == 'n3':
        return HttpResponse(resource.serialize(format='n3'), 
                mimetype='text/n3')
    elif format == 'nt':
        return HttpResponse(resource.serialize(format='nt'), 
                mimetype='text/plain')

