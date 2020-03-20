from enum import IntEnum

try:
    from enum import IntFlag
except ImportError:
    IntFlag = IntEnum


class AuthenticationMode(IntEnum):
    """AuthenticationMode indicates how a user authenticates to a PI Server

    Detailed information is available at :afsdk:`AF.PI.PIAuthenticationMode <T_OSIsoft_AF_PI_PIAuthenticationMode.htm>`.
    """

    #: Use Windows authentication when making a connection
    WINDOWS_AUTHENTICATION = 0
    #: Use the PI User authentication mode when making a connection
    PI_USER_AUTHENTICATION = 1


class CalculationBasis(IntEnum):
    """CalculationBasis indicates how values should be weighted over a time range

    Detailed information is available at :afsdk:`AF.Data.AFCalculationBasis <T_OSIsoft_AF_Data_AFCalculationBasis.htm>`.
    """

    #: Each event is weighted according to the time over which it applies.
    TIME_WEIGHTED = 0
    #: Each event is weighted equally.
    EVENT_WEIGHTED = 1
    #: Each event is time weighted, but interpolation is always done as if it is continous data.
    TIME_WEIGHTED_CONTINUOUS = 2
    #: Each event is time weighted, but interpolation is always done as if it is discrete, stepped, data.
    TIME_WEIGHTED_DISCRETE = 3
    #: Each event is weighted equally, except data at the end of the interval is excluded.
    EVENT_WEIGHTED_EXCLUDE_MOST_RECENT = 4
    #: Each event is weighted equally, except data at the beginning of the interval is excluded.
    EVENT_WEIGHTED_EXCLUDE_EARLIEST = 5
    #: Each event is weighted equally, data at both boundaries of the interval are explicitly included.
    EVENT_WEIGHTED_INCLUDE_BOTH_ENDS = 6


class ExpressionSampleType(IntEnum):
    """ExpressionSampleType indicates how expressions are evaluated over a time range.

    Detailed information is available at :afsdk:`AF.Data.AFSampleType <T_OSIsoft_AF_Data_AFSampleType.htm>`.
    """

    #: The expression is evaluated at each archive event.
    EXPRESSION_RECORDED_VALUES = 0
    #: The expression is evaluated at a sampling interval, passed as a separate argument.
    INTERVAL = 1


class RetrievalMode(IntEnum):
    """RetrievalMode indicates which recorded value should be returned

    Detailed information is available at :afsdk:`AF.Data.AFRetrievalMode <T_OSIsoft_AF_Data_AFRetrievalMode.htm>`.
    """

    #: Autmatic detection
    AUTO = 0
    #: At the exact time if available, else the first before the requested time
    AT_OR_BEFORE = 1
    #: The first before the requested time
    BEFORE = 6
    #: At the exact time if available, else the first after the requested time
    AT_OR_AFTER = 2
    #: The first after the requested time
    AFTER = 7
    #: At the exact time if available, else return an error
    EXACT = 4


class SummaryType(IntFlag):
    """SummaryType indicates which types of summary should be calculated.

    Based on :class:`enum.IntEnum` in Python 3.5 or earlier. `SummaryType`'s can
    be or'ed together. Python 3.6 or higher returns a new `IntFlag`, while in
    previous versions it will be casted down to `int`.

    >>> SummaryType.MINIMUM | SummaryType.MAXIMUM  # Returns minimum and maximum
    <SummaryType.MAXIMUM|MINIMUM: 12>  # On Python 3.6+
    12  # On previous versions

    Detailed information is available at :afsdk:`AF.Data.AFSummaryTypes <T_OSIsoft_AF_Data_AFSummaryTypes.htm>`.
    """

    #: No summary data
    NONE = 0
    #: A total over the time span
    TOTAL = 1
    #: Average value over the time span
    AVERAGE = 2
    #: The minimum value in the time span
    MINIMUM = 4
    #: The maximum value in the time span
    MAXIMUM = 8
    #: The range of the values (max-min) in the time span
    RANGE = 16
    #: The sample standard deviation of the values over the time span
    STD_DEV = 32
    #: The population standard deviation of the values over the time span
    POP_STD_DEV = 64
    #: The sum of the event count (when the calculation is event weighted). The sum of the event time duration (when the calculation is time weighted.)
    COUNT = 128
    #: The percentage of the data with a good value over the time range. Based on time for time weighted calculations, based on event count for event weigthed calculations.
    PERCENT_GOOD = 8192
    #: The total over the time span, with the unit of measurement that's associated with the input (or no units if not defined for the input).
    TOTAL_WITH_UOM = 16384
    #: A convenience to retrieve all summary types
    ALL = 24831
    #: A convenience to retrieve all summary types for non-numeric data
    ALL_FOR_NON_NUMERIC = 8320


class TimestampCalculation(IntEnum):
    """
    TimestampCalculation defines the timestamp returned for a given summary calculation

    Detailed information is available at :afsdk:`AF.Data.AFTimeStampCalculation <T_OSIsoft_AF_Data_AFTimestampCalculation.htm>`.
    """

    #: The timestamp is the event time of the minimum or maximum for those summaries or the beginning of the interval otherwise.
    AUTO = 0
    #: The timestamp is always the beginning of the interval.
    EARLIEST_TIME = 1
    #: The timestamp is always the end of the interval.
    MOST_RECENT_TIME = 2


def get_enumerated_value(enumeration, value, default):
    if not value:
        return default
    return enumeration(value)
