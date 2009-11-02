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

import kochief.cataloging.models as models
import kochief.cataloging.lib.mimeparse as mimeparse

def resource_view(request, resource_id, format='xml'):
    resource = models.Resource.objects.get(id=resource_id)
    available = ['text/plain']
    format_map = {
        'xml': 'application/rdf+xml',
        'n3': 'text/n3',
        'nt': 'text/plain',
    }
    available.append(format_map[format])
    accept = request.META.get('HTTP_ACCEPT', 'application/rdf+xml')
    match = mimeparse.best_match(available, accept)
    return http.HttpResponse(resource.serialize(format=format), 
            mimetype=match)

