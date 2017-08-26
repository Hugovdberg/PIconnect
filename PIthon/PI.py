""" PI
    Core containers for connections to PI databases
"""
from PIthon.AFSDK import AF
from PIData import PISeries
from PIthon._operators import add_operators, operators


class PIServer(object):
    """Context manager for connections to a PI server."""
    version = '0.2.1'

    servers = {server.Name: server for server in AF.PI.PIServers()}
    default_server = AF.PI.PIServers().DefaultPIServer

    def __init__(self, server=None):
        self.connection = self.servers.get(server, self.default_server)

    def __enter__(self):
        force_connection = False  # Don't force to retry connecting if previous attempt failed
        self.connection.Connect(force_connection)
        return self

    def __exit__(self, *args):
        self.connection.Disconnect()

    def __repr__(self):
        return u'%s(\\\\%s)' % (self.__class__.__name__, self.server_name)

    @property
    def server_name(self):
        """Return the name of the connected PI server as a string."""
        return self.connection.Name

    def search(self, query, source=None):
        """Search for tags on the connected PI server

           PI Points are matched to *query*, which can be provided as a string or
           a list of strings. In either case a single, unnested, list of
           Pithon.PI.PIPoints is returned.
        """
        if isinstance(query, list):
            return [y for x in query for y in self.search(x, source)]
        elif not isinstance(query, basestring):
            raise TypeError('Argument query must be either a string or a list of strings,' +
                            'got type ' + str(type(query)))
        return [PIPoint(pi_point) for pi_point in
                AF.PI.PIPoint.FindPIPoints(self.connection, query, source, None)]


@add_operators(
    operators=operators,
    members=[
        '_current_value',
        'sampled_data'
    ],
    newclassname='VirtualPIPoint',
    attributes=['pi_point']
)
class PIPoint(object):
    """Reference to a PI Point to get data and corresponding metadata from the server.

        TODO: Build a PI datacontainer from which PIPoint and PIAFAttribute subclass.
    """
    version = '0.2.0'

    __boundary_types = {
        'inside': AF.Data.AFBoundaryType.Inside,
        'outside': AF.Data.AFBoundaryType.Outside,
        'interpolate': AF.Data.AFBoundaryType.Interpolated
    }

    def __init__(self, pi_point):
        self.pi_point = pi_point
        self.tag = pi_point.Name
        self.__attributes_loaded = False
        self.__raw_attributes = {}

    def __repr__(self):
        return u'%s(%s, %s; Current Value: %s %s)' % (self.__class__.__name__,
                                                      self.tag,
                                                      self.description,
                                                      self.current_value,
                                                      self.units_of_measurement)

    def _current_value(self):
        """Return the last recorded value for this PI Point (internal use only)."""
        return self.pi_point.CurrentValue().Value

    @property
    def current_value(self):
        """Return the last recorded value for this PI Point."""
        return self._current_value()

    @property
    def last_update(self):
        """Return the time at which the last value for this PI Point was recorded."""
        return PISeries.timestamp_to_index(self.pi_point.CurrentValue().Timestamp.UtcTime)

    @property
    def raw_attributes(self):
        """Return a dictionary of the raw attributes of the PI Point."""
        self.__load_attributes()
        return self.__raw_attributes

    @property
    def units_of_measurement(self):
        """Return the units of measument in which values for this PI Point are reported."""
        self.__load_attributes()
        return self.__raw_attributes['engunits']

    @property
    def description(self):
        """Return the description of the PI Point.

        TODO: Add setter to alter displayed description
        """
        self.__load_attributes()
        return self.__raw_attributes['descriptor']

    def compressed_data(self,
                        start_time,
                        end_time,
                        boundary_type='inside',
                        filter_expression=None):
        """Return a PISeries of recorded data.

           Data is returned between the given *start_time* and *end_time*, inclusion
           of the boundaries is determined by the *boundary_type* attribute. Both
           *start_time* and *end_time* are parsed by AF.Time and allow for time
           specification relative to "now" by use of the asterisk.

           By default the *boundary_type* is set to 'inside', which returns from
           the first value after *start_time* to the last value before *end_time*.
           The other options are 'outside', which returns from the last value
           before *start_time* to the first value before *end_time*, and
           'interpolate', which interpolates the  first value to the given
           *start_time* and the last value to the given *end_time*.

           *filter_expression* is an optional string to filter the returned
           values, see OSIsoft PI documentation for more information.

           The AF SDK allows for inclusion of filtered data, with filtered values
           marked as such. At this point PIthon does not support this and filtered
           values are always left out entirely.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        if boundary_type.lower() in self.__boundary_types:
            boundary_type = self.__boundary_types[boundary_type.lower()]
        else:
            raise ValueError(
                'Argument boundary_type must be one of ' + ', '.join(
                    '"%s"' % x for x in sorted(self.__boundary_types.keys())
                )
            )
        include_filtered_values = False  # Leave out values excluded by filter_expression
        pivalues = self.pi_point.RecordedValues(time_range,
                                                boundary_type,
                                                filter_expression,
                                                include_filtered_values)
        timestamps, values = [], []
        for value in pivalues:
            timestamps.append(PISeries.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        return PISeries(tag=self.tag,
                        timestamp=timestamps,
                        value=values,
                        uom=self.units_of_measurement)

    def sampled_data(self,
                     start_time,
                     end_time,
                     interval,
                     filter_expression=None):
        """Return a PISeries of interpolated data.

           Data is returned between *start_time* and *end_time* at a fixed
           *interval*. All three values are parsed by AF.Time and the first two
           allow for time specification relative to "now" by use of the asterisk.

           *filter_expression* is an optional string to filter the returned
           values, see OSIsoft PI documentation for more information.

           The AF SDK allows for inclusion of filtered data, with filtered values
           marked as such. At this point PIthon does not support this and filtered
           values are always left out entirely.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        include_filtered_values = False
        pivalues = self.pi_point.InterpolatedValues(time_range,
                                                    interval,
                                                    filter_expression,
                                                    include_filtered_values)
        timestamps, values = [], []
        for value in pivalues:
            timestamps.append(PISeries.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        return PISeries(tag=self.tag,
                        timestamp=timestamps,
                        value=values,
                        uom=self.units_of_measurement)

    def __load_attributes(self):
        """Load the raw attributes of the PI Point from the server"""
        if not self.__attributes_loaded:
            self.pi_point.LoadAttributes([])
            self.__attributes_loaded = True
        self.__raw_attributes = {att.Key: att.Value for att in self.pi_point.GetAttributes([])}

    def _current_value(self):
        """Return the last recorded value for this PI Point (internal use only)."""
        return self.pi_point.CurrentValue().Value
