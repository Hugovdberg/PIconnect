"""Test communication with the PI AF system"""
# Copyright 2017 Hugo van den Berg, Stijn de Jong

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# pragma pylint: disable=unused-import
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str,
                      ascii, chr, hex, input, next, oct, open,
                      pow, round, super,
                      filter, map, zip)
# pragma pylint: enable=unused-import

import PIconnect as PI
from PIconnect.test.fakes import VirtualTestCase


class TestAFDatabase(VirtualTestCase):
    """Test connecting to the AF database"""

    def test_connection(self):
        """Test that creating a PI.PIAFDatabase object without arguments raises no exception"""
        try:
            PI.PIAFDatabase()
        except Exception as e:
            self.fail("PI.PIAFDatabase() raised %s unexpectedly." %
                      e.__class__.__name__)

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        AFserver = PI.AF.PISystems().DefaultPISystem.Name
        database = PI.AF.PISystems().DefaultPISystem.Databases.DefaultDatabase.Name
        server = PI.PIAFDatabase(AFserver, database)
        self.assertEqual(server.server_name,
                         AFserver)
        self.assertEqual(server.database_name,
                         'TestDatabase')
        self.assertEqual(repr(server),
                         'PIAFDatabase(\\\\{s}\\{d})'.format(s=AFserver, d=database))

    def test_unknown_server_name(self):
        """Test that the server reports a warning for an unknown server."""
        AFserver_name = '__'.join(
            [name for name in PI.PIAFDatabase.servers] +
            ['UnkownServerName']
        )
        with self.assertWarns(UserWarning):
            PI.PIAFDatabase(server=AFserver_name)

    def test_unknown_database_name(self):
        """Test that the server reports a warning for an unknown database."""
        server = PI.PIAFDatabase.default_server['server']
        databases = [db.Name for db in server.Databases]
        AFdatabase_name = '__'.join(databases + ['UnkownDatabaseName'])
        with self.assertWarns(UserWarning):
            PI.PIAFDatabase(database=AFdatabase_name)


class TestDatabaseDescendants(VirtualTestCase):
    """Test retrieving child elements"""

    def test_children(self):
        """Test that calling children on the database returns a dict of child elements"""
        with PI.PIAFDatabase() as db:
            children = db.children
        self.assertIsInstance(children, dict)
