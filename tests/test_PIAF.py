"""Test communication with the PI AF system."""

from typing import cast

import pytest

import PIconnect as PI
import PIconnect.AFSDK as AFSDK
import PIconnect.PIAF as PIAF
from PIconnect._typing import AF

AFSDK.AF, AFSDK.System, AFSDK.AF_SDK_VERSION = AFSDK.__fallback()
PI.AF = PIAF.AF = AFSDK.AF
PI.PIAFDatabase.servers = PIAF._lookup_servers()
PI.PIAFDatabase.default_server = PIAF._lookup_default_server()


class TestAFDatabase:
    """Test connecting to the AF database."""

    def test_connection(self):
        """Test creating a PI.PIAFDatabase object without arguments raises no exception."""
        PI.PIAFDatabase()

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        AFserver = PI.AF.PISystems().DefaultPISystem.Name
        database = PI.AF.PISystems().DefaultPISystem.Databases.DefaultDatabase.Name
        server = PI.PIAFDatabase(AFserver, database)
        assert server.server_name == AFserver
        assert server.database_name == database
        assert repr(server) == "PIAFDatabase(\\\\{s}\\{d})".format(s=AFserver, d=database)

    def test_unknown_server_name(self):
        """Test that the server reports a warning for an unknown server."""
        AFserver_name = "__".join(list(PI.PIAFDatabase.servers) + ["UnkownServerName"])
        with pytest.warns(UserWarning):
            PI.PIAFDatabase(server=AFserver_name)

    def test_unknown_database_name(self):
        """Test that the server reports a warning for an unknown database."""
        server = cast(AF.PISystem, PI.PIAFDatabase.default_server["server"])  # type: ignore
        databases = [db.Name for db in server.Databases]
        AFdatabase_name = "__".join(databases + ["UnkownDatabaseName"])
        with pytest.warns(UserWarning):
            PI.PIAFDatabase(database=AFdatabase_name)


class TestDatabaseDescendants:
    """Test retrieving child elements."""

    def test_children(self):
        """Test that calling children on the database returns a dict of child elements."""
        with PI.PIAFDatabase() as db:
            children = db.children
        assert isinstance(children, dict)


class TestDatabaseSearch:
    """Test retrieving attributes."""

    def test_search(self):
        """Test that calling attributes on the database returns a list of attributes."""
        with PI.PIAFDatabase() as db:
            attributes = db.search([r"", r""])
        assert isinstance(attributes, list)

    def test_split_element_attribute(self):
        """Test that calling attributes on the database returns a list of attributes."""
        with PI.PIAFDatabase() as db:
            attributes = db.search(r"BaseElement|Attribute1")
        assert attributes[0].name == "Attribute1"

    def test_split_element_nested_attribute(self):
        """Test that calling attributes on the database returns a list of attributes."""
        with PI.PIAFDatabase() as db:
            attributes = db.search(r"BaseElement|Attribute1|Attribute2")
        assert attributes[0].name == "Attribute2"
