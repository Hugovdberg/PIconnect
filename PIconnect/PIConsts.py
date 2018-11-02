from enum import IntFlag, IntEnum


class _IntFlag(IntFlag):
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def get_item(cls, value, default=None):
        for item in cls:
            if value == item.value:
                return item
        else:
            return default


class _IntEnum(IntEnum):
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def get_item(cls, value, default=None):
        for item in cls:
            if value == item.value:
                return item
        else:
            return default


class SummaryType(_IntFlag):
    NONE = 0
    TOTAL = 1
    AVERAGE = 2
    MINIMUM = 4
    MAXIMUM = 8
    RANGE = 16
    STD_DEV = 32
    POP_STD_DEV = 64
    COUNT = 128
    PERCENT_GOOD = 8192
    TOTAL_WITH_UOM = 16384
    ALL = 24831
    ALL_FOR_NON_NUMERIC = 8320


class CalculationBasis(_IntEnum):
    TIME_WEIGHTED = 0
    EVENT_WEIGHTED = 1
    TIME_WEIGHTED_CONTINUOUS = 2
    TIME_WEIGHTED_DISCRETE = 3
    EVENT_WEIGHTED_EXCLUDE_MOST_RECENT = 4
    EVENT_WEIGHTED_EXCLUDE_EARLIEST = 5
    EVENT_WEIGHTED_INCLUDE_BOTH_ENDS = 6


class TimestampCalculation(_IntEnum):
    AUTO = 0
    EARLIEST_TIME = 1
    MOST_RECENT_TIME = 2
