"""Type hints for the AF.Data module.

Contains various enumerations and classes for data retrieval.
"""

import enum

from . import Generic, Time
from . import UnitsOfMeasure as UOM
from ._values import AFValue, AFValues


class AFBoundaryType(enum.IntEnum):
    """Mock class of the AF.Data.AFBoundaryType enumeration."""

    Inside = 0
    Outside = 1
    Interpolated = 2


class AFBufferOption(enum.IntEnum):
    """Mock class of the AF.Data.AFBufferOption enumeration."""

    DoNotBuffer = 0
    BufferIfPossible = 1
    Buffer = 2


class AFCalculationBasis(enum.IntEnum):
    """Mock class of the AF.Data.AFCalculationBasis enumeration."""

    TimeWeighted = 0
    EventWeighted = 1
    TimeWeightedContinuous = 2
    TimeWeightedDiscrete = 3
    EventWeightedExcludeMostRecentEvent = 4
    EventWeightedExcludeEarliestEvent = 5
    EventWeightedIncludeBothEnds = 6


class AFRetrievalMode(enum.IntEnum):
    Auto = 0
    AtOrBefore = 1
    Before = 6
    AtOrAfter = 2
    After = 7
    Exact = 4


class AFSampleType(enum.IntEnum):
    """Mock class of the AF.Data.AFSampleType enumeration."""

    ExpressionRecordedValues = 0
    Interval = 1


class AFSummaryTypes(enum.IntEnum):
    """Mock class of the AF.Data.AFSummaryTypes enumeration."""

    None_ = 0
    Total = 1
    Average = 2
    Minimum = 4
    Maximum = 8
    Range = 16
    StdDev = 32
    PopulationStdDev = 64
    Count = 128
    PercentGood = 8192
    TotalWithUOM = 16384
    All = 24831
    AllForNonNumeric = 8320


class AFTimestampCalculation(enum.IntEnum):
    """Mock class of the AF.Data.AFTimestampCalculation enumeration."""

    Auto = 0
    EarliestTime = 1
    MostRecentTime = 2


class AFUpdateOption(enum.IntEnum):
    """Mock class of the AF.Data.AFUpdateOption enumeration."""

    Replace = 0
    Insert = 4
    NoReplace = 2
    ReplaceOnly = 3
    InsertNoCompression = 5
    Remove = 6


SummariesDict = Generic.Dictionary[AFSummaryTypes, AFValues]
SummaryDict = Generic.Dictionary[AFSummaryTypes, AFValue]


class AFData:
    """Mock class of the AF.Data.AFData class."""

    @staticmethod
    def FilteredSummaries(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        filter_expression: str,
        summary_types: AFSummaryTypes,
        calculation_basis: AFCalculationBasis,
        filter_evaluation: AFSampleType,
        filter_interval: Time.AFTimeSpan,
        time_type: AFTimestampCalculation,
        /,
    ) -> SummariesDict:
        return SummariesDict([])

    @staticmethod
    def InterpolatedValue(
        time: Time.AFTime,
        uom: UOM.UOM,
        /,
    ) -> AFValue:
        return AFValue(None, time)

    @staticmethod
    def InterpolatedValues(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        uom: UOM.UOM,
        filter_expression: str,
        include_filtered_values: bool,
        /,
    ) -> AFValues:
        return AFValues()

    @staticmethod
    def RecordedValue(
        time: Time.AFTime,
        retrieval_mode: AFRetrievalMode,
        uom: UOM.UOM,
        /,
    ) -> AFValue:
        return AFValue(None, time)

    @staticmethod
    def RecordedValues(
        time_range: Time.AFTimeRange,
        boundary_type: AFBoundaryType,
        uom: UOM.UOM,
        filter_expression: str,
        include_filtered_values: bool,
        /,
    ) -> AFValues:
        return AFValues()

    @staticmethod
    def Summaries(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        summary_type: AFSummaryTypes,
        calculation_basis: AFCalculationBasis,
        time_type: AFTimestampCalculation,
        /,
    ) -> SummariesDict:
        return SummariesDict([])

    @staticmethod
    def Summary(
        time_range: Time.AFTimeRange,
        summary_type: AFSummaryTypes,
        calculation_basis: AFCalculationBasis,
        time_type: AFTimestampCalculation,
        /,
    ) -> SummaryDict:
        return SummaryDict([])

    @staticmethod
    def UpdateValue(
        value: AFValue,
        update_option: AFUpdateOption,
        buffer_option: AFBufferOption,
        /,
    ) -> None:
        pass
