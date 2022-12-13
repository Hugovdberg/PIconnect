from typing import List

from . import Asset, Data, Generic, Time


class PIPoint:
    """Mock class of the AF.PI.PIPoint class"""

    Name: str = "TestPIPoint"
    """This property identifies the name of the PIPoint"""

    @staticmethod
    def CurrentValue() -> Asset.AFValue:
        return Asset.AFValue(None)

    @staticmethod
    def FilteredSummaries(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        filter_expression: str,
        summary_type: Data.AFSummaryTypes,
        calculation_basis: Data.AFCalculationBasis,
        sample_type: Data.AFSampleType,
        sample_interval: Time.AFTimeSpan,
        time_type: Data.AFTimestampCalculation,
        /,
    ) -> Generic.SummariesDict:
        return Generic.SummariesDict([])

    @staticmethod
    def FindPIPoints(connection, query, source, attribute_names) -> List["PIPoint"]:
        """Stub to mock querying PIPoints"""
        return []

    @staticmethod
    def GetAttributes(names: List[str], /) -> Generic.PropertyDict:
        return Generic.PropertyDict([])

    @staticmethod
    def InterpolatedValue(time: Time.AFTime, /) -> Asset.AFValue:
        return Asset.AFValue(None, time)

    @staticmethod
    def InterpolatedValues(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        filter_expression: str,
        include_filtered_values: bool,
        /,
    ) -> Asset.AFValues:
        return Asset.AFValues()

    @staticmethod
    def LoadAttributes(params: List[str], /) -> None:
        pass

    @staticmethod
    def RecordedValue(
        time: Time.AFTime, retrieval_mode: Data.AFRetrievalMode, /
    ) -> Asset.AFValue:
        return Asset.AFValue(None, time)

    @staticmethod
    def RecordedValues(
        time_range: Time.AFTimeRange,
        boundary_type: Data.AFBoundaryType,
        filter_expression: str,
        include_filtered_values: bool,
        max_count: int = 0,
        /,
    ) -> Asset.AFValues:
        return Asset.AFValues()

    @staticmethod
    def Summaries(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        summary_type: Data.AFSummaryTypes,
        calculation_basis: Data.AFCalculationBasis,
        time_type: Data.AFTimestampCalculation,
        /,
    ) -> Generic.SummariesDict:
        return Generic.SummariesDict([])

    @staticmethod
    def Summary(
        time_range: Time.AFTimeRange,
        summary_type: Data.AFSummaryTypes,
        calculation_basis: Data.AFCalculationBasis,
        time_type: Data.AFTimestampCalculation,
    ) -> Generic.SummariesDict:
        return Generic.SummariesDict([])

    @staticmethod
    def UpdateValue(
        value: Asset.AFValue,
        update_mode: Data.AFUpdateOption,
        buffer_option: Data.AFBufferOption,
        /,
    ) -> None:
        pass


class PIServer:
    """Mock class of the AF.PI.PIServer class"""

    def __init__(self, name):
        self.Name = name

    def Connect(self, retry):
        """Stub for connecting to test server"""

    def Disconnect(self):
        """Stub for disconnecting from test server"""


class PIServers:
    """Mock class of the AF.PI.PIServers class"""

    DefaultPIServer = PIServer("Testing")

    def __iter__(self):
        return (x for x in [self.DefaultPIServer])
