"""Mock classes of the AF.PI namespace of the OSIsoft PI-AF SDK"""
from typing import Iterable, Iterator, List, Optional

from . import Asset, Data, Generic, Time

__all__ = ["PIPoint", "PIServer", "PIServers"]


class PIServer:
    """Mock class of the AF.PI.PIServer class"""

    def __init__(self, name: str) -> None:
        self.Name = name
        self._connected = False

    def Connect(self, retry: bool) -> None:
        """Stub for connecting to test server"""
        self._connected = True

    def Disconnect(self) -> None:
        """Stub for disconnecting from test server"""
        self._connected = False


class PIServers:
    """Mock class of the AF.PI.PIServers class"""

    def __init__(self) -> None:
        self.DefaultPIServer = PIServer("Testing")

    def __iter__(self) -> Iterator[PIServer]:
        return (x for x in [self.DefaultPIServer])


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
    ) -> Asset.SummariesDict:
        return Asset.SummariesDict([])

    @staticmethod
    def FindPIPoints(
        connection: PIServer,
        query: str,
        source: Optional[str],
        attribute_names: Optional[Iterable[str]],
    ) -> Iterable["PIPoint"]:
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
    ) -> Asset.SummariesDict:
        return Asset.SummariesDict([])

    @staticmethod
    def Summary(
        time_range: Time.AFTimeRange,
        summary_type: Data.AFSummaryTypes,
        calculation_basis: Data.AFCalculationBasis,
        time_type: Data.AFTimestampCalculation,
    ) -> Asset.SummaryDict:
        return Asset.SummaryDict([])

    @staticmethod
    def UpdateValue(
        value: Asset.AFValue,
        update_mode: Data.AFUpdateOption,
        buffer_option: Data.AFBufferOption,
        /,
    ) -> None:
        pass
