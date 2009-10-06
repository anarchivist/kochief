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

"""Ingests documents into the catalog."""

import optparse
from optparse import make_option
import urllib

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from kochief.cataloging import models

NTRIPLE_FILE = 'tmp.nt'
RDF_FILE = 'tmp.rdf'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-p', '--parser',
            dest='parser',
            metavar='PARSER', 
            help='Use PARSER (in kochief/cataloging/parsers) to parse FILEs for ingesting'),
    )
    help = 'Ingests documents into the catalog.'
    args = 'file_or_url [file_or_url ...]'

    def handle(self, *file_or_urls, **options):
        if file_or_urls:
            parser_module = options.get('parser')
            parser = None
            if parser_module:
                if parser_module.endswith('.py'):
                    parser_module = parser_module[:-3]
                parser = __import__('kochief.cataloging.parsers.' + parser_module, globals(), 
                        locals(), [parser_module])
        for file_or_url in file_or_urls:
            data_handle = urllib.urlopen(file_or_url)
            # committer is "machine" from fixture
            #committer = User.objects.get(id=2)
            if not parser:
                # guess parser based on file extension
                if file_or_url.endswith('.mrc'):
                    import kochief.cataloging.parsers.marc as parser
                else:
                    raise CommandError("Please specify a parser.")
            #out_handle = open(RDF_FILE, 'w')
            #count = parser.write_graph(data_handle, out_handle, format='xml')
            count = 0
            for record in parser.generate_records(data_handle):
                count += 1
                statements = parser.get_statements(record)
                resource = models.Resource(record['id'], statements)
                resource.save()

            #    db_record.save()
            #    id = db_record.id
            #    print "Saving record %s" % id
            #    record['id'] = id
            #    db_record.version_set.create(
            #        data=simplejson.dumps(record), 
            #        message='record %s created by ingest' % id,
            #        committer=committer,
            #    )
            print
            print "%s records saved" % count

