"""Test communication with the PI AF system"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str,
                      ascii, chr, hex, input, next, oct, open,
                      pow, round, super,
                      filter, map, zip)

import PIconnect as PI
from PIconnect.test.fakes import VirtualTestCase


class TestAFDatabase(VirtualTestCase):
    """Test connecting to the AF database"""

    def test_connection(self):
        """Test that creating a PI.PIAFDatabase object without arguments raises no exception"""
        try:
            PI.PIAFDatabase()
        except Exception as e:
            self.fail("PI.PIAFDatabase() raised %s unexpectedly." % e.__class__.__name__)

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        AFserver = PI.AF.PISystems().DefaultPISystem.Name
        database = PI.AF.PISystems().DefaultPISystem.Databases.DefaultDatabase.Name
        server = PI.PIAFDatabase(AFserver, database)
        self.assertEqual(server.server_name,
                         AFserver)
        self.assertEqual(server.database_name,
                         'BasisStructuur')
        self.assertEqual(repr(server),
                         'PIAFDatabase(\\\\{s}\\{d})'.format(s=AFserver, d=database))


class TestDatabaseDescendants(VirtualTestCase):
    """Test retrieving child elements"""

    def test_children(self):
        """Test that calling children on the database returns a dict of child elements"""
        with PI.PIAFDatabase() as db:
            children = db.children
        self.assertIsInstance(children, dict)
