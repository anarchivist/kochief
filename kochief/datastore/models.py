# Copyright 2009 Gabriel Farrell
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

import rdflib
from rdflib import plugin
from rdflib.store import Store
from rdflib.Graph import ConjunctiveGraph as Graph

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils import simplejson

from kochief import settings

DB_MAP = {
    'sqlite3': 'SQLite',
}

DEFAULT_GRAPH_URI = settings.BASE_URL + 'rdf'

STORE = plugin.get(DB_MAP[settings.DATABASE_ENGINE], Store)(
        settings.DATABASE_NAME)
RT = STORE.open('', create=False)
STORE_GRAPH = Graph(STORE, identifier = rdflib.URIRef(DEFAULT_GRAPH_URI))

LOCALNS = rdflib.Namespace(settings.BASE_URL + 'resource/')

# TODO: timestamps for triples

class Resource(object):
    def __init__(self, subject=None, statements=None):
        ''' 
        statements is a list of tuples, each corresponding to a statement
        abount the subject.
        '''
        self.subject = subject
        self.statements = statements

    def get_existing_statements(self):
        return STORE_GRAPH.query(
            'SELECT ?p ?o WHERE {localns:%s ?p ?o.}' % self.subject, 
            initNs={'localns': LOCALNS})

    def save(self):
        # find intersection of self.fields and self.existing
        # remove self.existing not in intersection
        # add self.fields not in intersection
        for statement in self.statements:
            STORE_GRAPH.add((LOCALNS[self.subject], LOCALNS[statement[0]],
                rdflib.Literal(statement[1])))
        STORE_GRAPH.commit()
    
    def delete(self):
        pass

def get_resource(id):
    subject = LOCALNS[id]
    statements = STORE_GRAPH.predicate_objects(subject)
    resource_graph = Graph(identifier = rdflib.URIRef(DEFAULT_GRAPH_URI))
    for statement in statements:
        resource_graph.add((subject, statement[0], statement[1]))
    return resource_graph


#class Record(models.Model):
#    def __unicode__(self):
#        return unicode(self.id)
#
#    def get_current(self):
#        return self.get_versions()[0]
#
#    def get_versions(self):
#        return self.version_set.order_by('-id')
#
#class Version(models.Model):
#    record = models.ForeignKey(Record)
#    data = models.TextField()
#    timestamp = models.DateTimeField(auto_now_add=True)
#    message = models.CharField(max_length=256)
#    committer = models.ForeignKey(User)
#
#    class Meta:
#        ordering = ['-timestamp']
#
#    def __unicode__(self):
#        return self.message
#
#    def get_data(self):
#        return simplejson.loads(self.data)
#
#class VersionInline(admin.TabularInline):
#    model = Version
#    extra = 1
#
#class RecordAdmin(admin.ModelAdmin):
#    inlines = [VersionInline]
#
#admin.site.register(Record, RecordAdmin)
#admin.site.register(Version)
