"""Test communication with the PI AF system"""
# pragma pylint: disable=unused-import
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import (
    ascii,
    bytes,
    chr,
    dict,
    filter,
    hex,
    input,
    int,
    list,
    map,
    next,
    object,
    oct,
    open,
    pow,
    range,
    round,
    str,
    super,
    zip,
)

import pytest

import PIconnect as PI

# pragma pylint: enable=unused-import


class TestAFDatabase:
    """Test connecting to the AF database"""

    def test_connection(self):
        """Test that creating a PI.PIAFDatabase object without arguments raises no exception"""
        PI.PIAFDatabase()

    def test_server_name(self):
        """Test that the server reports the same name as which was connected to."""
        AFserver = PI.AF.PISystems().DefaultPISystem.Name
        database = PI.AF.PISystems().DefaultPISystem.Databases.DefaultDatabase.Name
        server = PI.PIAFDatabase(AFserver, database)
        assert server.server_name == AFserver
        assert server.database_name == database
        assert repr(server) == "PIAFDatabase(\\\\{s}\\{d})".format(
            s=AFserver, d=database
        )

    def test_unknown_server_name(self):
        """Test that the server reports a warning for an unknown server."""
        AFserver_name = "__".join(
            [name for name in PI.PIAFDatabase.servers] + ["UnkownServerName"]
        )
        with pytest.warns(UserWarning):
            PI.PIAFDatabase(server=AFserver_name)

    def test_unknown_database_name(self):
        """Test that the server reports a warning for an unknown database."""
        server = PI.PIAFDatabase.default_server["server"]
        databases = [db.Name for db in server.Databases]
        AFdatabase_name = "__".join(databases + ["UnkownDatabaseName"])
        with pytest.warns(UserWarning):
            PI.PIAFDatabase(database=AFdatabase_name)


class TestDatabaseDescendants:
    """Test retrieving child elements"""

    def test_children(self):
        """Test that calling children on the database returns a dict of child elements"""
        with PI.PIAFDatabase() as db:
            children = db.children
        assert isinstance(children, dict)
