import enum


class AFBoundaryType(enum.IntEnum):
    """Mock class of the AF.Data.AFBoundaryType enumeration"""

    Inside = 0
    Outside = 1
    Interpolated = 2


class AFBufferOption(enum.IntEnum):
    """Mock class of the AF.Data.AFBufferOption enumeration"""

    DoNotBuffer = 0
    BufferIfPossible = 1
    Buffer = 2


class AFCalculationBasis(enum.IntEnum):
    """Mock class of the AF.Data.AFCalculationBasis enumeration"""

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
    """Mock class of the AF.Data.AFSampleType enumeration"""

    ExpressionRecordedValues = 0
    Interval = 1


class AFSummaryTypes(enum.IntEnum):
    """Mock class of the AF.Data.AFSummaryTypes enumeration"""

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
    """Mock class of the AF.Data.AFTimestampCalculation enumeration"""

    Auto = 0
    EarliestTime = 1
    MostRecentTime = 2


class AFUpdateOption(enum.IntEnum):
    """Mock class of the AF.Data.AFUpdateOption enumeration"""

    Replace = 0
    Insert = 4
    NoReplace = 2
    ReplaceOnly = 3
    InsertNoCompression = 5
    Remove = 6
