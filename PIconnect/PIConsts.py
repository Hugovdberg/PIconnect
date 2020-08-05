from enum import IntEnum

try:
    from enum import IntFlag
except ImportError:
    IntFlag = IntEnum


class CalculationBasis(IntEnum):
    """CalculationBasis indicates how values should be weighted over a time range

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_Data_AFCalculationBasis.htm
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

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_Data_AFSampleType.htm
    """

    #: The expression is evaluated at each archive event.
    EXPRESSION_RECORDED_VALUES = 0
    #: The expression is evaluated at a sampling interval, passed as a separate argument.
    INTERVAL = 1


class SummaryType(IntFlag):
    """SummaryType indicates which types of summary should be calculated.

    Based on :class:`enum.IntEnum` in Python 3.5 or earlier. `SummaryType`'s can
    be or'ed together. Python 3.6 or higher returns a new `IntFlag`, while in
    previous versions it will be casted down to `int`.

    >>> SummaryType.MINIMUM | SummaryType.MAXIMUM  # Returns minimum and maximum
    <SummaryType.MAXIMUM|MINIMUM: 12>  # On Python 3.6+
    12  # On previous versions

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_Data_AFSummaryTypes.htm
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

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_Data_AFTimestampCalculation.htm
    """

    #: The timestamp is the event time of the minimum or maximum for those summaries or the beginning of the interval otherwise.
    AUTO = 0
    #: The timestamp is always the beginning of the interval.
    EARLIEST_TIME = 1
    #: The timestamp is always the end of the interval.
    MOST_RECENT_TIME = 2

class UpdateOption(IntEnum):
    """ 
    Indicates how to treat duplicate values in the archive, when supported by the Data Reference 

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_Data_AFUpdateOption.htm
    """
    # Add the value to the archive. If any values exist at the same time, will overwrite one of them and set its Substituted flag.
    REPLACE = 0
    # Add the value to the archive. Any existing values at the same time are not overwritten.
    INSERT = 1
    # Add the value to the archive only if no value exists at the same time. If a value already exists for that time, the passed value is ignored.
    NOREPLACE = 2
    # Replace an existing value in the archive at the specified time. If no existing value is found, the passed value is ignored.
    REPLACEONLY = 3
    # Add the value to the archive without compression. If this value is written to the snapshot, the previous snapshot value will be written to the archive, 
    # without regard to compression settings. Note that if a subsequent snapshot value is written without the InsertNoCompression option, 
    # the value added with the InsertNoCompression option is still subject to compression.
    INSERTNOCOMPRESSION = 5
    # Remove the value from the archive if a value exists at the passed time.
    REMOVE = 6

class BufferOption(IntEnum):
    """
    Indicates buffering option in updating values, when supported by the Data Reference.

    Detailed information is available at https://techsupport.osisoft.com/Documentation/PI-AF-SDK/html/T_OSIsoft_AF_Data_AFBufferOption.htm
    """
    # Updating data reference values without buffer.
    DONOTBUFFER	= 0
    # Try updating data reference values with buffer. If fails (e.g. data reference AFDataMethods does not support Buffering, or its Buffering system is not available), then try updating directly without buffer.
    BUFFERIFPOSSIBLE = 1
    # Updating data reference values with buffer.
    BUFFER = 2
    
def get_enumerated_value(enumeration, value, default):
    if not value:
        return default
    return enumeration(value)
