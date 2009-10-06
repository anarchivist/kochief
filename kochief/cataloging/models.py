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

import rdflib.graph as rg
import rdflib.namespace as ns
import rdflib.term as rt

import django.conf as conf

DB_MAP = {
    'mysql': 'MySQL',
    'postgresql': 'PostgreSQL',
    'postgresql_psycopg2': 'PostgreSQL',
    'sqlite3': 'SQLite',
}
LOCALNS = ns.Namespace(conf.settings.LOCALNS)
STORE_GRAPH = rg.ConjunctiveGraph(DB_MAP[conf.settings.DATABASE_ENGINE], 
        identifier=LOCALNS)
# TODO: graph configuration for mysql/postgresql
STORE_GRAPH.open(conf.settings.DATABASE_NAME, create=True)

class ResourceManager(object):
    """Manager for resource objects."""

    def all(self):
        return STORE_GRAPH

    def filter(self, sparql_query):
        return STORE_GRAPH.query(sparql_query)

    def get(self, id):
        subject = LOCALNS[id]
        statements = STORE_GRAPH.predicate_objects(subject)
        resource = Resource(id, statements)
        return resource
        

class Resource(object):
    """Model for a resource in the catalonging."""
    objects = ResourceManager()

    def __init__(self, id, statements=None):
        self.id = id
        self.subject = LOCALNS[id]
        self.statements = statements
        self.graph = self.get_graph()

    def delete(self):
        pass

    def get_graph(self):
        graph = rg.Graph()
        for statement in self.statements:
            graph.add((self.subject, statement[0], statement[1]))
        return graph

    def get_existing_statements(self):
        return STORE_GRAPH.predicate_objects(self.subject)

    def save(self):
        # TODO: copy self.existing to store_graph of old revisions
        # remove self.existing and add self.statements 
        for statement in self.statements:
            STORE_GRAPH.add((self.subject, statement[0], statement[1]))
        STORE_GRAPH.commit()
    
    def serialize(self, format='xml'):
        return self.graph.serialize(format=format)

