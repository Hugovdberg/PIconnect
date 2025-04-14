"""Test communication with the PI AF system."""

from typing import cast

import pytest

import PIconnect as PI
from PIconnect import Asset, dotnet
from PIconnect._typing import AF

dotnet.lib.load_test_SDK()


class TestAFDatabase:
    """Test connecting to the AF database."""

    def test_connection(self):
        """Test creating a PI.AFDatabase object without arguments raises no exception."""
        PI.AFDatabase()

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        AFserver = dotnet.lib.AF.PISystems().DefaultPISystem.Name
        database = dotnet.lib.AF.PISystems().DefaultPISystem.Databases.DefaultDatabase.Name
        server = PI.AFDatabase(AFserver, database)
        assert server.server_name == AFserver
        assert server.database_name == database
        assert repr(server) == "AFDatabase(\\\\{s}\\{d})".format(s=AFserver, d=database)

    def test_unknown_server_name(self):
        """Test that the server reports a warning for an unknown server."""
        AFserver_name = "__".join(list(PI.AFDatabase.servers()) + ["UnkownServerName"])
        with pytest.warns(UserWarning):
            PI.AFDatabase(server=AFserver_name)

    def test_unknown_database_name(self):
        """Test that the server reports a warning for an unknown database."""
        server = cast(AF.PISystem, PI.AFDatabase.default_server())  # type: ignore
        databases = [db.Name for db in server.Databases]
        AFdatabase_name = "__".join(databases + ["UnkownDatabaseName"])
        with pytest.warns(UserWarning):
            PI.AFDatabase(database=AFdatabase_name)


class TestDatabaseDescendants:
    """Test retrieving child elements."""

    def test_children(self):
        """Test that calling children on the database returns a dict of child elements."""
        with PI.AFDatabase() as db:
            children = db.children
            assert isinstance(children, dict)


class TestDatabaseSearch:
    """Test retrieving attributes."""

    def test_search(self):
        """Test that calling attributes on the database returns a list of attributes."""
        with pytest.warns(DeprecationWarning):
            with PI.AFDatabase() as db:
                attributes = db.search([r"", r""])
                assert isinstance(attributes, Asset.AFAttributeList)

    def test_split_element_attribute(self):
        """Test that calling attributes on the database returns a list of attributes."""
        with pytest.warns(DeprecationWarning):
            with PI.AFDatabase() as db:
                print(db.children)
                attributes = db.search(r"BaseElement|Attribute1")
                assert isinstance(attributes[0].name, str)

    def test_split_element_nested_attribute(self):
        """Test that calling attributes on the database returns a list of attributes."""
        with pytest.warns(DeprecationWarning):
            with PI.AFDatabase() as db:
                attributes = db.search(r"BaseElement|Attribute1|Attribute2")
                assert isinstance(attributes[0].name, str)
