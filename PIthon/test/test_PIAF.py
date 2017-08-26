"""Test communication with the PI AF system"""
import PIthon as PI
from PIthon.test.fakes import VirtualTestCase


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
        server = PI.PIAFDatabase('PIAF_server', 'BasisStructuur')
        self.assertEqual(server.server_name, 'PIAF_server')

    def test_database_name(self):
        """Test that the server reports the same name as which was connected to."""
        server = PI.PIAFDatabase('PIAF_server', 'BasisStructuur')
        self.assertEqual(server.database_name, 'BasisStructuur')

    def test_repr(self):
        """Test that the server representation matches the connected server."""
        server = PI.PIAFDatabase('PIAF_server', 'BasisStructuur')
        self.assertEqual(repr(server), 'PIAFDatabase(\\\\PIAF_server\\BasisStructuur)')


class TestDatabaseDescendants(VirtualTestCase):
    """Test retrieving child elements"""

    def test_children(self):
        """Test that calling children on the database returns a dict of child elements"""
        with PI.PIAFDatabase() as db:
            children = db.children
        self.assertIsInstance(children, dict)
