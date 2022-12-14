""" PI
    Core containers for connections to PI databases
"""
import warnings
from typing import Any, Dict, List, Optional, Union, cast

import PIconnect._typing.AF as _AFtyping
import PIconnect._typing.Generic as _dotNetGeneric
from PIconnect import AF, PIConsts, PIData, _time
from PIconnect._operators import OPERATORS, add_operators  # type: ignore
from PIconnect._utils import InitialisationWarning

__all__ = ["PIPoint", "PIServer"]


def _lookup_servers() -> Dict[str, AF.PI.PIServer]:
    servers: Dict[str, AF.PI.PIServer] = {}
    from System import Exception as dotNetException  # type: ignore

    for server in AF.PI.PIServers():
        try:
            servers[server.Name] = server
        except (Exception, dotNetException) as e:  # type: ignore
            warnings.warn(
                f"Failed loading server data for {server.Name} "
                f"with error {type(cast(Exception, e)).__qualname__}",
                InitialisationWarning,
            )
    return servers


def _lookup_default_server() -> Optional[AF.PI.PIServer]:

    default_server = None
    try:
        default_server = AF.PI.PIServers().DefaultPIServer
    except Exception:
        warnings.warn("Could not load the default PI Server", ResourceWarning)
    return default_server


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
    servers = _lookup_servers()
    #: Default server, as reported by the SDK
    default_server = _lookup_default_server()

    def __init__(
        self,
        server: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        domain: Optional[str] = None,
        authentication_mode: PIConsts.AuthenticationMode = PIConsts.AuthenticationMode.PI_USER_AUTHENTICATION,
        timeout: Optional[int] = None,
    ) -> None:
        if server is None:
            if self.default_server is None:
                raise ValueError(
                    "No server was specified and no default server was found."
                )
            self.connection = self.default_server
        elif server not in self.servers:
            if self.default_server is None:
                raise ValueError(
                    f"Server '{server}' not found and no default server was found."
                )
            message = 'Server "{server}" not found, using the default server.'
            warnings.warn(message=message.format(server=server), category=UserWarning)
            self.connection = self.default_server
        else:
            self.connection = self.servers[server]

        if bool(username) != bool(password):
            raise ValueError(
                "When passing credentials both the username and password must be specified."
            )
        if domain and not username:
            raise ValueError(
                "A domain can only specified together with a username and password."
            )
        if username:
            from System.Net import NetworkCredential  # type: ignore
            from System.Security import SecureString  # type: ignore

            secure_pass = cast(_dotNetGeneric.SecureString, SecureString())
            if password is not None:
                for c in password:
                    secure_pass.AppendChar(c)
            cred = [username, secure_pass] + ([domain] if domain else [])
            self._credentials = (
                cast(_dotNetGeneric.NetworkCredential, NetworkCredential(*cred)),
                AF.PI.PIAuthenticationMode(int(authentication_mode)),
            )
        else:
            self._credentials = None

        if timeout:
            from System import TimeSpan  # type: ignore

            # System.TimeSpan(hours, minutes, seconds)
            self.connection.ConnectionInfo.OperationTimeOut = cast(
                _dotNetGeneric.TimeSpan, TimeSpan(0, 0, timeout)
            )

    def __enter__(self):
        if self._credentials:
            self.connection.Connect(*self._credentials)
        else:
            # Don't force to retry connecting if previous attempt failed
            force_connection = False
            self.connection.Connect(force_connection)
        return self

    def __exit__(self, *args: Any):
        self.connection.Disconnect()

    def __repr__(self) -> str:
        return "%s(\\\\%s)" % (self.__class__.__name__, self.server_name)

    @property
    def server_name(self):
        """server_name

        Name of the connected server
        """
        return self.connection.Name

    def search(
        self, query: Union[str, List[str]], source: Optional[str] = None
    ) -> List["PIPoint"]:
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
                self.connection, str(query), source, None
            )
        ]


@add_operators(
    operators=OPERATORS,
    members=["_current_value", "interpolated_values"],
    newclassname="VirtualPIPoint",
    attributes=["pi_point"],
)
class PIPoint(PIData.PISeriesContainer):
    """PIPoint

    Reference to a PI Point to get data and corresponding metadata from the server.

    Args:
        pi_point (AF.PI.PIPoint): Reference to a PIPoint as returned by the SDK
    """

    version = "0.3.0"

    def __init__(self, pi_point: AF.PI.PIPoint) -> None:
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
    def created(self):
        """Return the creation datetime of a point."""
        return _time.timestamp_to_index(self.raw_attributes["creationdate"])

    @property
    def description(self):
        """Return the description of the PI Point.

        .. todo::

            Add setter to alter displayed description
        """
        return self.raw_attributes["descriptor"]

    @property
    def last_update(self):
        """Return the time at which the last value for this PI Point was recorded."""
        return _time.timestamp_to_index(self.pi_point.CurrentValue().Timestamp.UtcTime)

    @property
    def name(self) -> str:
        return self.tag

    @property
    def raw_attributes(self) -> Dict[str, Any]:
        """Return a dictionary of the raw attributes of the PI Point."""
        self.__load_attributes()
        return self.__raw_attributes

    @property
    def units_of_measurement(self) -> Optional[str]:
        """Return the units of measument in which values for this PI Point are reported."""
        return self.raw_attributes["engunits"]

    def __load_attributes(self) -> None:
        """Load the raw attributes of the PI Point from the server"""
        if not self.__attributes_loaded:
            self.pi_point.LoadAttributes([])
            self.__attributes_loaded = True
        self.__raw_attributes = {
            att.Key: att.Value for att in self.pi_point.GetAttributes([])
        }

    def _current_value(self) -> Any:
        """Return the last recorded value for this PI Point (internal use only)."""
        return self.pi_point.CurrentValue().Value

    def _filtered_summaries(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        filter_expression: str,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        filter_evaluation: AF.Data.AFSampleType,
        filter_interval: AF.Time.AFTimeSpan,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
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

    def _interpolated_value(self, time: AF.Time.AFTime) -> AF.Asset.AFValue:
        """Return a single value for this PI Point"""
        return self.pi_point.InterpolatedValue(time)

    def _interpolated_values(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
        """Internal function to actually query the pi point"""
        include_filtered_values = False
        return self.pi_point.InterpolatedValues(
            time_range, interval, filter_expression, include_filtered_values
        )

    def _normalize_filter_expression(self, filter_expression: str) -> str:
        return filter_expression.replace("%tag%", self.tag)

    def _recorded_value(
        self, time: AF.Time.AFTime, retrieval_mode: AF.Data.AFRetrievalMode
    ) -> AF.Asset.AFValue:
        """Return a single value for this PI Point"""
        return self.pi_point.RecordedValue(
            time, AF.Data.AFRetrievalMode(int(retrieval_mode))
        )

    def _recorded_values(
        self,
        time_range: AF.Time.AFTimeRange,
        boundary_type: AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
        include_filtered_values = False
        return self.pi_point.RecordedValues(
            time_range, boundary_type, filter_expression, include_filtered_values
        )

    def _summary(
        self,
        time_range: AF.Time.AFTimeRange,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        return self.pi_point.Summary(
            time_range, summary_types, calculation_basis, time_type
        )

    def _summaries(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.pi_point.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _update_value(
        self,
        value: AF.Asset.AFValue,
        update_mode: AF.Data.AFUpdateOption,
        buffer_mode: AF.Data.AFBufferOption,
    ) -> None:
        return self.pi_point.UpdateValue(value, update_mode, buffer_mode)
