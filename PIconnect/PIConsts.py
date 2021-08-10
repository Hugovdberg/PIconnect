from enum import IntEnum

try:
    from enum import IntFlag
except ImportError:
    IntFlag = IntEnum


class UpdateMode(IntEnum):
    """Indicates how to treat duplicate values in the archive, when supported by the Data Reference.

    Detailed information is available at :afsdk:`AF.Data.AFUpdateOption <T_OSIsoft_AF_Data_AFUpdateOption.htm>`
    """

    #: Add the value to the archive.
    #: If any values exist at the same time, will overwrite one of them and set its Substituted flag.
    REPLACE = 0
    #: Add the value to the archive. Any existing values at the same time are not overwritten.
    INSERT = 1
    #: Add the value to the archive only if no value exists at the same time.
    #: If a value already exists for that time, the passed value is ignored.
    NO_REPLACE = 2
    #: Replace an existing value in the archive at the specified time.
    #: If no existing value is found, the passed value is ignored.
    REPLACE_ONLY = 3
    #: Add the value to the archive without compression.
    #: If this value is written to the snapshot, the previous snapshot value will be written to the archive,
    #: without regard to compression settings.
    #: Note that if a subsequent snapshot value is written without the InsertNoCompression option,
    #: the value added with the InsertNoCompression option is still subject to compression.
    INSERT_NO_COMPRESSION = 5
    #: Remove the value from the archive if a value exists at the passed time.
    REMOVE = 6


class BufferMode(IntEnum):
    """Indicates buffering option in updating values, when supported by the Data Reference.

    Detailed information is available at :afsdk:`AF.Data.AFBufferOption <T_OSIsoft_AF_Data_AFBufferOption.htm>`
    """

    #: Updating data reference values without buffer.
    DO_NOT_BUFFER = 0
    #: Try updating data reference values with buffer.
    #: If fails (e.g. data reference AFDataMethods does not support Buffering, or its Buffering system is not available),
    #: then try updating directly without buffer.
    BUFFER_IF_POSSIBLE = 1
    # Updating data reference values with buffer.
    BUFFER = 2


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


class EventFrameSearchMode(IntEnum):
    """EventFrameSearchMode

    EventFrameSearchMode defines the interpretation and direction from the start time
    when searching for event frames.

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_EventFrame_AFEventFrameSearchMode.htm,
    including a graphical display of event frames that are returned for a given search
    mode.
    """

    #: Uninitialized
    NONE = 0
    #: Backward from start time, also known as starting before
    BACKWARD_FROM_START_TIME = 1
    STARTING_BEFORE = 1
    #: Forward from start time, also known as starting after
    FORWARD_FROM_START_TIME = 2
    STARTING_AFTER = 2
    #: Backward from end time, also known as ending before
    BACKWARD_FROM_END_TIME = 3
    ENDING_BEFORE = 3
    #: Forward from end time, also known as ending after
    FORWARD_FROM_END_TIME = 4
    ENDING_AFTER = 4
    #: Backward in progress, also known as starting before and in progress
    BACKWARD_IN_PROGRESS = 5
    STARTING_BEFORE_IN_PROGRESS = 5
    #: Forward in progress, also known as starting after and in progress
    FORWARD_IN_PROGRESS = 6
    STARTING_AFTER_IN_PROGRESS = 6


def get_enumerated_value(enumeration, value, default):
    if not value:
        return default
    return enumeration(value)
