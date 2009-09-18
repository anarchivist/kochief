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

"""Parser for xrecords."""

import urllib
from xml.etree.ElementTree import ElementTree

URL_TEMPLATE = 'http://innopac.library.drexel.edu/xrecord=%s'

def get_record(record_id, url_template=URL_TEMPLATE):
    xrecord = urllib.urlopen(url_template % record_id)
    tree = ElementTree()
    tree.parse(xrecord)
    def join_subfields(field):
        subdata_list = field.findall('MARCSUBFLD/SUBFIELDDATA')
        value = ' '.join([x.text for x in subdata_list])
        return value
    def get_sub_a(field):
        subfields = field.findall('MARCSUBFLD')
        for sub in subfields:
            ind = sub.findtext('SUBFIELDINDICATOR')
            if ind == 'a':
                return sub.findtext('SUBFIELDDATA')

    tag_map = {
        '090': [('call_number', join_subfields)],
        '245': [('full_title', join_subfields), 
                ('title', get_sub_a)],
        '250': [('edition', get_sub_a)],
        '260': [('imprint', join_subfields)],
    }

    var_fields = tree.findall('VARFLD')
    field_list = []
    for field in var_fields:
        tag = field.findtext('MARCINFO/MARCTAG')
        for name, value_func in tag_map.get(tag, []):
            field_list.append((name, value_func(field)))
    for name, value in field_list:
        print name, value

if __name__ == '__main__':
    get_record('b1402870')


