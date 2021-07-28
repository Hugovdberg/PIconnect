""" PIAF
    Core containers for connections to the PI Asset Framework.
"""
# pragma pylint: disable=unused-import, redefined-builtin
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

try:
    from __builtin__ import str as BuiltinStr
except ImportError:
    BuiltinStr = str
# pragma pylint: enable=unused-import, redefined-builtin
from warnings import warn

from PIconnect._operators import OPERATORS, add_operators
from PIconnect.AFSDK import AF
from PIconnect.PIData import PISeries, PISeriesContainer
from PIconnect._utils import classproperty

_NOTHING = object()


class PIAFDatabase(object):
    """PIAFDatabase

    Context manager for connections to the PI Asset Framework database.
    """

    version = "0.1.2"

    _servers = _NOTHING
    _default_server = _NOTHING

    def __init__(self, server=None, database=None):
        self.server = None
        self.database = None
        self._initialise_server(server)
        self._initialise_database(database)

    @classproperty
    def servers(self):
        if self._servers is _NOTHING:
            i, j, failed_servers, failed_databases = 0, 0, 0, 0
            self._servers = {}
            for i, s in enumerate(AF.PISystems(), start=1):
                try:
                    self._servers[s.Name] = {"server": s, "databases": {}}
                    for j, d in enumerate(s.Databases, start=1):
                        try:
                            self._servers[s.Name]["databases"][d.Name] = d
                        except Exception:
                            failed_databases += 1
                except Exception:
                    failed_servers += 1
            if failed_servers or failed_databases:
                warn(
                    "Failed loading {}/{} servers and {}/{} databases".format(
                        failed_servers, i, failed_databases, j
                    )
                )
        return self._servers

    @classproperty
    def default_server(self):
        if self._default_server is _NOTHING:
            self._default_server = None
            if AF.PISystems().DefaultPISystem:
                self._default_server = self.servers[AF.PISystems().DefaultPISystem.Name]
            elif len(self.servers) > 0:
                self._default_server = self.servers[list(self.servers)[0]]
            else:
                self._default_server = None
        return self._default_server

    def _initialise_server(self, server):
        if server and server not in self.servers:
            message = 'Server "{server}" not found, using the default server.'
            warn(message=message.format(server=server), category=UserWarning)
        server = self.servers.get(server, self.default_server)
        self.server = server["server"]

    def _initialise_database(self, database):
        server = self.servers.get(self.server.Name)
        if not server["databases"]:
            server["databases"] = {x.Name: x for x in self.server.Databases}
        if database and database not in server["databases"]:
            message = 'Database "{database}" not found, using the default database.'
            warn(message=message.format(database=database), category=UserWarning)
        default_db = self.server.Databases.DefaultDatabase
        self.database = server["databases"].get(database, default_db)

    def __enter__(self):
        self.server.Connect()
        return self

    def __exit__(self, *args):
        pass
        # Disabled disconnecting because garbage collection sometimes impedes
        # connecting to another server later
        # self.server.Disconnect()

    def __repr__(self):
        return "%s(\\\\%s\\%s)" % (
            self.__class__.__name__,
            self.server_name,
            self.database_name,
        )

    @property
    def server_name(self):
        """Return the name of the connected PI AF server."""
        return self.server.Name

    @property
    def database_name(self):
        """Return the name of the connected PI AF database."""
        return self.database.Name

    @property
    def children(self):
        """Return a dictionary of the direct child elements of the database."""
        return {c.Name: PIAFElement(c) for c in self.database.Elements}

    def descendant(self, path):
        """Return a descendant of the database from an exact path."""
        return PIAFElement(self.database.Elements.get_Item(path))


class PIAFElement(object):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)

    @property
    def name(self):
        """Return the name of the current element."""
        return self.element.Name

    @property
    def parent(self):
        """Return the parent element of the current element, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self):
        """Return a dictionary of the direct child elements of the current element."""
        return {c.Name: self.__class__(c) for c in self.element.Elements}

    def descendant(self, path):
        """Return a descendant of the current element from an exact path."""
        return self.__class__(self.element.Elements.get_Item(path))

    @property
    def attributes(self):
        """Return a dictionary of the attributes of the current element."""
        return {a.Name: PIAFAttribute(self, a) for a in self.element.Attributes}


@add_operators(
    operators=OPERATORS,
    members=["_current_value", "interpolated_values"],
    newclassname="VirtualPIAFAttribute",
    attributes=["element", "attribute"],
)
class PIAFAttribute(PISeriesContainer):
    """Container for attributes of PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, element, attribute):
        super().__init__()
        self.element = element
        self.attribute = attribute

    def __repr__(self):
        return "%s(%s, %s; Current Value: %s %s)" % (
            self.__class__.__name__,
            self.name,
            self.description,
            self.current_value,
            self.units_of_measurement,
        )

    @property
    def name(self):
        """Return the name of the current attribute."""
        return self.attribute.Name

    @property
    def parent(self):
        """Return the parent attribute of the current attribute, or None if it has none."""
        if not self.attribute.Parent:
            return None
        return self.__class__(self.element, self.attribute.Parent)

    @property
    def children(self):
        """Return a dictionary of the direct child attributes of the current attribute."""
        return {
            a.Name: self.__class__(self.element, a) for a in self.attribute.Attributes
        }

    @property
    def description(self):
        """Return the description of the PI Point."""
        return self.attribute.Description

    @property
    def last_update(self):
        """Return the time at which the current_value was last updated."""
        return PISeries.timestamp_to_index(self.attribute.GetValue().Timestamp.UtcTime)

    @property
    def units_of_measurement(self):
        """Return the units of measurement in which values for this element are reported."""
        return self.attribute.DefaultUOM

    def _current_value(self):
        return self.attribute.GetValue().Value

    def _interpolated_value(self, time):
        return self.attribute.Data.InterpolatedValue(time, self.attribute.DefaultUOM)

    def _recorded_value(self, time, retrieval_mode):
        return self.attribute.Data.RecordedValue(
            time, int(retrieval_mode), self.attribute.DefaultUOM
        )

    def _recorded_values(self, time_range, boundary_type, filter_expression):
        include_filtered_values = False
        return self.attribute.Data.RecordedValues(
            time_range,
            boundary_type,
            self.attribute.DefaultUOM,
            filter_expression,
            include_filtered_values,
        )

    def _interpolated_values(self, time_range, interval, filter_expression):
        """Internal function to actually query the pi point"""
        include_filtered_values = False
        return self.attribute.Data.InterpolatedValues(
            time_range,
            interval,
            self.attribute.DefaultUOM,
            filter_expression,
            include_filtered_values,
        )

    def _summary(self, time_range, summary_types, calculation_basis, time_type):
        return self.attribute.Data.Summary(
            time_range, summary_types, calculation_basis, time_type
        )

    def _summaries(
        self, time_range, interval, summary_types, calculation_basis, time_type
    ):
        return self.attribute.Data.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _filtered_summaries(
        self,
        time_range,
        interval,
        filter_expression,
        summary_types,
        calculation_basis,
        filter_evaluation,
        filter_interval,
        time_type,
    ):
        return self.attribute.Data.FilteredSummaries(
            time_range,
            interval,
            filter_expression,
            summary_types,
            calculation_basis,
            filter_evaluation,
            filter_interval,
            time_type,
        )
