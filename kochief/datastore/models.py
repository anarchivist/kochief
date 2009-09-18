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

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils import simplejson

DB_MAP = {
    'mysql': 'MySQL',
    'postgresql': 'PostgreSQL',
    'postgresql_psycopg2': 'PostgreSQL',
    'sqlite3': 'SQLite',
}
STORE = plugin.get(DB_MAP[settings.DATABASE_ENGINE], Store)(
        settings.DATABASE_NAME)
RT = STORE.open('', create=False)
DEFAULT_GRAPH_URI = settings.LOCALNS
STORE_GRAPH = Graph(STORE, 
        identifier = rdflib.URIRef(DEFAULT_GRAPH_URI))
LOCALNS = rdflib.Namespace(settings.LOCALNS)

# TODO: timestamps for triples

class Resource(object):
    def __init__(self, id=None, statements=None):
        ''' 
        statements is a set of triples, each corresponding to a statement
        about the subject.
        '''
        self.id = id
        self.subject = LOCALNS[id]
        self.statements = statements

    def get_existing_statements(self):
        return STORE_GRAPH.predicate_objects(self.subject)

    def save(self):
        # find intersection of self.fields and self.existing
        # remove self.existing not in intersection
        # add self.fields not in intersection
        for statement in self.statements:
            STORE_GRAPH.add(statement)
        STORE_GRAPH.commit()
    
    def delete(self):
        pass

def get_resource(id):
    if id:
        subject = LOCALNS[id]
        statements = STORE_GRAPH.predicate_objects(subject)
        resource_graph = Graph()
        for statement in statements:
            resource_graph.add((subject, statement[0], statement[1]))
    else:
        resource_graph = STORE_GRAPH
    return resource_graph

