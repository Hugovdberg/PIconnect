""" PI
    Core containers for connections to PI databases
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
from PIconnect._utils import classproperty
from PIconnect.AFSDK import AF
from PIconnect.PIConsts import AuthenticationMode
from PIconnect.PIData import PISeriesContainer
from PIconnect.time import timestamp_to_index

_NOTHING = object()


class PIServer(object):  # pylint: disable=useless-object-inheritance
    """PIServer is a connection to an OSIsoft PI Server

    Args:
        server (str, optional): Name of the server to connect to, defaults to None
        username (str, optional): can be used only with password as well
        password (str, optional): -//-
        todo: domain, auth
        timeout (int, optional): the maximum seconds an operation can take

    .. note::
        If the specified `server` is unknown a warning is thrown and the connection
        is redirected to the default server, as if no server was passed. The list
        of known servers is available in the `PIServer.servers` dictionary.
    """

    version = "0.2.2"

    #: Dictionary of known servers, as reported by the SDK
    _servers = _NOTHING
    #: Default server, as reported by the SDK
    _default_server = _NOTHING

    def __init__(
        self,
        server=None,
        username=None,
        password=None,
        domain=None,
        authentication_mode=AuthenticationMode.PI_USER_AUTHENTICATION,
        timeout=None,
    ):
        if server and server not in self.servers:
            message = 'Server "{server}" not found, using the default server.'
            warn(message=message.format(server=server), category=UserWarning)
        if bool(username) != bool(password):
            raise ValueError(
                "When passing credentials both the username and password must be specified."
            )
        if domain and not username:
            raise ValueError(
                "A domain can only specified together with a username and password."
            )
        if username:
            from System.Net import NetworkCredential
            from System.Security import SecureString

            secure_pass = SecureString()
            for c in password:
                secure_pass.AppendChar(c)
            cred = [username, secure_pass] + ([domain] if domain else [])
            self._credentials = (NetworkCredential(*cred), int(authentication_mode))
        else:
            self._credentials = None

        self.connection = self.servers.get(server, self.default_server)

        if timeout:
            from System import TimeSpan

            # System.TimeSpan(hours, minutes, seconds)
            self.connection.ConnectionInfo.OperationTimeOut = TimeSpan(0, 0, timeout)

    @classproperty
    def servers(self):
        if self._servers is _NOTHING:
            i, failures = 0, 0
            self._servers = {}
            for i, server in enumerate(AF.PI.PIServers(), start=1):
                try:
                    self._servers[server.Name] = server
                except Exception:
                    failures += 1
            if failures:
                warn(
                    "Could not load {} PI Server(s) out of {}".format(failures, i),
                    ResourceWarning,
                )
        return self._servers

    @classproperty
    def default_server(self):
        if self._default_server is _NOTHING:
            self._default_server = None
            try:
                self._default_server = AF.PI.PIServers().DefaultPIServer
            except Exception:
                warn("Could not load the default PI Server", ResourceWarning)
        return self._default_server

    def __enter__(self):
        if self._credentials:
            self.connection.Connect(*self._credentials)
        else:
            # Don't force to retry connecting if previous attempt failed
            force_connection = False
            self.connection.Connect(force_connection)
        return self

    def __exit__(self, *args):
        self.connection.Disconnect()

    def __repr__(self):
        return "%s(\\\\%s)" % (self.__class__.__name__, self.server_name)

    @property
    def server_name(self):
        """server_name

        Name of the connected server
        """
        return self.connection.Name

    def search(self, query, source=None):
        """search

        Search PIPoints on the PIServer

        Args:
            query (str or [str]): String or list of strings with queries
            source (str, optional): Defaults to None. Point source to limit the results

        Returns:
            list: A list of :class:`PIPoint` objects as a result of the query

        .. todo::

            Reject searches while not connected
        """
        if isinstance(query, list):
            return [y for x in query for y in self.search(x, source)]
        # elif not isinstance(query, str):
        #     raise TypeError('Argument query must be either a string or a list of strings,' +
        #                     'got type ' + str(type(query)))
        return [
            PIPoint(pi_point)
            for pi_point in AF.PI.PIPoint.FindPIPoints(
                self.connection, BuiltinStr(query), source, None
            )
        ]


@add_operators(
    operators=OPERATORS,
    members=["_current_value", "interpolated_values"],
    newclassname="VirtualPIPoint",
    attributes=["pi_point"],
)
class PIPoint(PISeriesContainer):
    """PIPoint

    Reference to a PI Point to get data and corresponding metadata from the server.

    Args:
        pi_point (AF.PI.PIPoint): Reference to a PIPoint as returned by the SDK
    """

    version = "0.3.0"

    def __init__(self, pi_point):
        super().__init__()
        self.pi_point = pi_point
        self.tag = pi_point.Name
        self.__attributes_loaded = False
        self.__raw_attributes = {}

    def __repr__(self):
        return "%s(%s, %s; Current Value: %s %s)" % (
            self.__class__.__name__,
            self.tag,
            self.description,
            self.current_value,
            self.units_of_measurement,
        )

    @property
    def last_update(self):
        """Return the time at which the last value for this PI Point was recorded."""
        return timestamp_to_index(self.pi_point.CurrentValue().Timestamp.UtcTime)

    @property
    def raw_attributes(self):
        """Return a dictionary of the raw attributes of the PI Point."""
        self.__load_attributes()
        return self.__raw_attributes

    @property
    def units_of_measurement(self):
        """Return the units of measument in which values for this PI Point are reported."""
        self.__load_attributes()
        return self.__raw_attributes["engunits"]

    @property
    def description(self):
        """Return the description of the PI Point.

        .. todo::

            Add setter to alter displayed description
        """
        self.__load_attributes()
        return self.__raw_attributes["descriptor"]

    def __load_attributes(self):
        """Load the raw attributes of the PI Point from the server"""
        if not self.__attributes_loaded:
            self.pi_point.LoadAttributes([])
            self.__attributes_loaded = True
        self.__raw_attributes = {
            att.Key: att.Value for att in self.pi_point.GetAttributes([])
        }

    @property
    def name(self):
        return self.tag

    def _current_value(self):
        """Return the last recorded value for this PI Point (internal use only)."""
        return self.pi_point.CurrentValue().Value

    def _interpolated_value(self, time):
        """Return a single value for this PI Point"""
        return self.pi_point.InterpolatedValue(time)

    def _recorded_value(self, time, retrieval_mode):
        """Return a single value for this PI Point"""
        return self.pi_point.RecordedValue(time, int(retrieval_mode))

    def _update_value(self, value, update_mode, buffer_mode):
        return self.pi_point.UpdateValue(value, update_mode, buffer_mode)

    def _recorded_values(self, time_range, boundary_type, filter_expression):
        include_filtered_values = False
        return self.pi_point.RecordedValues(
            time_range, boundary_type, filter_expression, include_filtered_values
        )

    def _interpolated_values(self, time_range, interval, filter_expression):
        """Internal function to actually query the pi point"""
        include_filtered_values = False
        return self.pi_point.InterpolatedValues(
            time_range, interval, filter_expression, include_filtered_values
        )

    def _summary(self, time_range, summary_types, calculation_basis, time_type):
        return self.pi_point.Summary(
            time_range, summary_types, calculation_basis, time_type
        )

    def _summaries(
        self, time_range, interval, summary_types, calculation_basis, time_type
    ):
        return self.pi_point.Summaries(
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
        return self.pi_point.FilteredSummaries(
            time_range,
            interval,
            filter_expression,
            summary_types,
            calculation_basis,
            filter_evaluation,
            filter_interval,
            time_type,
        )

    def _normalize_filter_expression(self, filter_expression):
        return filter_expression.replace("%tag%", self.tag)
