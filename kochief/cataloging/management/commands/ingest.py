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

import csv
import optparse
import sys
import urllib

import django.conf as conf
import django.core.management.base as mb

import kochief.cataloging.models as models

CSV_FILE = 'tmp.csv'
NTRIPLE_FILE = 'tmp.nt'
RDF_FILE = 'tmp.rdf'
DISCOVERY_INSTALLED = 'kochief.discovery' in conf.settings.INSTALLED_APPS

class Command(mb.BaseCommand):
    option_list = mb.BaseCommand.option_list + (
        optparse.make_option('-p', '--parser',
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
                    raise mb.CommandError("Please specify a parser.")
            #out_handle = open(RDF_FILE, 'w')
            #count = parser.write_graph(data_handle, out_handle, format='xml')
            count = 0
            if DISCOVERY_INSTALLED:
                csv_handle = open(CSV_FILE, 'w')
                writer = csv.DictWriter(csv_handle, parser.FIELDNAMES)
                fieldname_dict = {}
                for fieldname in parser.FIELDNAMES:
                    fieldname_dict[fieldname] = fieldname
                writer.writerow(fieldname_dict)
            for record in parser.generate_records(data_handle):
                count += 1
                statements = record.get_statements()
                resource = models.Resource(record.id, statements)
                resource.save()

                if DISCOVERY_INSTALLED:
                    row = record.get_row()
                    writer.writerow(row)

                if count % 1000:
                    sys.stderr.write(".")
                else:
                    sys.stderr.write(str(count))
            data_handle.close()
            print
            print "%s records saved" % count
            if DISCOVERY_INSTALLED:
                csv_handle.close()
                import kochief.discovery.management.commands.index as i
                i.load_solr(CSV_FILE)
                os.remove(CSV_FILE)

