''' PI
    Core containers for connections to PI databases
'''
from AFSDK import AF
from PIData import PISeries

class PIServer(object):
    ''' A context manager for connections to a PI server
    '''

    version = '0.2.0'

    servers = {server.Name: server for server in AF.PI.PIServers()}
    default_server = AF.PI.PIServers().DefaultPIServer

    def __init__(self, server = None):
        self.connection = self.servers.get(server, self.default_server)

    def __enter__(self):
        force_connection = False # Don't force to retry connecting if previous attempt failed
        self.connection.Connect(force_connection)
        return self

    def __exit__(self, *args):
        self.connection.Disconnect()

    def __repr__(self):
        return u'%s(\\\\%s)' % (self.__class__.__name__, self.server_name)

    @property
    def server_name(self):
        ''' String containing the name of the connected PI server
        '''
        return self.connection.Name

    def search(self, query, source = None):
        ''' Searches for tags matching a querystring or a list of querystrings
            on the connected server
        '''
        findPIPoints = AF.PI.PIPoint.FindPIPoints
        if isinstance(query, list):
            pi_points, queries = [], query
            for query in queries:
                pi_points.extend(self.search(query, source))
            return pi_points
        elif not isinstance(query, basestring):
            raise TypeError('Argument query must be either a string or a list of strings')

        return [PIPoint(pi_point) for pi_point in findPIPoints(self.connection,
                                                               query,
                                                               source,
                                                               None)]

class PIPoint(object):
    ''' A reference to a PI Point to get data and corresponding metadata from the server
    '''

    version = '0.1.0'

    __boundary_types = {
        'inside': AF.Data.AFBoundaryType.Inside,
        'outside': AF.Data.AFBoundaryType.Outside,
        'interpolate': AF.Data.AFBoundaryType.Interpolated
    }

    def __init__(self, pi_point):
        self.pi_point = pi_point
        self.tag = pi_point.Name
        self.__attributes_loaded = False

    def __repr__(self):
        return u'%s(%s, %s; Current Value: %s %s)' % (self.__class__.__name__,
                                                      self.tag,
                                                      self.description,
                                                      self.current_value,
                                                      self.units_of_measurement)

    @property
    def current_value(self):
        ''' The current value that the PI Point reports, the units of measurment can be
            retrieved through the units_of_measurement property
        '''
        return self.pi_point.CurrentValue().Value

    @property
    def raw_attributes(self):
        ''' A dict of the raw attributes of the PI Point as reported by the server
        '''
        self.__load_attributes()
        return self.__raw_attributes

    @property
    def units_of_measurement(self):
        ''' The units of measument in which the values for this PI Point are reported
        '''
        self.__load_attributes()
        return self.__raw_attributes['engunits']

    @property
    def description(self):
        ''' The description of the PI Point
        '''
        self.__load_attributes()
        return self.__raw_attributes['descriptor']

    def compressed_data(self,
                        start_time,
                        end_time,
                        boundary_type='inside',
                        filter_expression=None):
        ''' compressed_data returns a PISeries of the data as stored on the server
            between the given *start_time* and *end_time*.

            By default the *boundary_type* is set to 'inside', which returns from
            the first value after *start_time* to the last value before *end_time*.
            The other options are 'outside', which returns from the last value
            before *start_time* to the first value before *end_time*, and
            'interpolate', which interpolates the  first value to the given
            *start_time* and the last value to the given *end_time*.

            *filter_expression* is an optional string to filter the returned
            values, see OSIsoft PI documentation for more information.
        '''
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        if boundary_type.lower() in self.__boundary_types:
            boundary_type = self.__boundary_types[boundary_type.lower()]
        else:
            raise ValueError('Argument boundary_type must be one of ' +
                             ', '.join(sorted(boundary_types.keys())))
        include_filtered_values = False # Leave out values excluded by filter_expression
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

    def sampled_data(self, start_time, end_time, interval):
        '''
        '''
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        pivalues = self.pi_point.InterpolatedValues(time_range, interval, "", False)
        timestamps, values = [], []
        for value in pivalues:
            timestamps.append(PISeries.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)

        return PISeries(tag=self.tag,
                        timestamp=timestamps,
                        value=values,
                        uom=self.units_of_measurement)

    def __load_attributes(self):
        if not self.__attributes_loaded:
            self.pi_point.LoadAttributes([])
            self.__attributes_loaded = True
        self.__raw_attributes = {att.Key: att.Value for att in self.pi_point.GetAttributes([])}
