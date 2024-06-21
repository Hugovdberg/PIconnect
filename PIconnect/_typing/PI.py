"""Mock classes of the AF.PI namespace of the OSIsoft PI-AF SDK."""

import enum
from typing import Iterable, Iterator, List, Optional, Union

from . import Data, Generic, Time, _values
from . import dotnet as System

__all__ = ["PIPoint", "PIServer", "PIServers"]


class PIConnectionInfo:
    """Mock class of the AF.PI.PIConnectionInfo class."""

    def __init__(self) -> None:
        self.OperationTimeOut: System.TimeSpan


class PIAuthenticationMode(enum.IntEnum):
    """Mock class of the AF.PI.PIAuthenticationMode class."""

    WindowsAuthentication = 0
    PIUserAuthentication = 1


class PIServer:
    """Mock class of the AF.PI.PIServer class."""

    def __init__(self, name: str) -> None:
        self.ConnectionInfo = PIConnectionInfo()
        self.Name = name
        self._connected = False

    def Connect(
        self,
        retry: Union[bool, System.Net.NetworkCredential],
        authentication_mode: Optional[PIAuthenticationMode] = None,
    ) -> None:
        """Stub for connecting to test server."""
        self._connected = True

    def Disconnect(self) -> None:
        """Stub for disconnecting from test server."""
        self._connected = False


class PIServers:
    """Mock class of the AF.PI.PIServers class."""

    def __init__(self) -> None:
        self.DefaultPIServer = PIServer("Testing")

    def __iter__(self) -> Iterator[PIServer]:
        return (x for x in [self.DefaultPIServer])


class PIPoint:
    """Mock class of the AF.PI.PIPoint class."""

    Name: str = "TestPIPoint"
    """This property identifies the name of the PIPoint"""

    @staticmethod
    def CurrentValue() -> _values.AFValue:
        return _values.AFValue(None)

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
    ) -> Data.SummariesDict:
        return Data.SummariesDict([])

    @staticmethod
    def FindPIPoints(
        connection: PIServer,
        query: str,
        source: Optional[str],
        attribute_names: Optional[Iterable[str]],
    ) -> Iterable["PIPoint"]:
        """Stub to mock querying PIPoints."""
        return []

    @staticmethod
    def GetAttributes(names: List[str], /) -> Generic.PropertyDict:
        return Generic.PropertyDict([])

    @staticmethod
    def InterpolatedValue(time: Time.AFTime, /) -> _values.AFValue:
        return _values.AFValue(None, time)

    @staticmethod
    def InterpolatedValues(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        filter_expression: str,
        include_filtered_values: bool,
        /,
    ) -> _values.AFValues:
        return _values.AFValues()

    @staticmethod
    def LoadAttributes(params: List[str], /) -> None:
        pass

    @staticmethod
    def RecordedValue(
        time: Time.AFTime, retrieval_mode: Data.AFRetrievalMode, /
    ) -> _values.AFValue:
        return _values.AFValue(None, time)

    @staticmethod
    def RecordedValues(
        time_range: Time.AFTimeRange,
        boundary_type: Data.AFBoundaryType,
        filter_expression: str,
        include_filtered_values: bool,
        max_count: int = 0,
        /,
    ) -> _values.AFValues:
        return _values.AFValues()

    @staticmethod
    def Summaries(
        time_range: Time.AFTimeRange,
        interval: Time.AFTimeSpan,
        summary_type: Data.AFSummaryTypes,
        calculation_basis: Data.AFCalculationBasis,
        time_type: Data.AFTimestampCalculation,
        /,
    ) -> Data.SummariesDict:
        return Data.SummariesDict([])

    @staticmethod
    def Summary(
        time_range: Time.AFTimeRange,
        summary_type: Data.AFSummaryTypes,
        calculation_basis: Data.AFCalculationBasis,
        time_type: Data.AFTimestampCalculation,
    ) -> Data.SummaryDict:
        return Data.SummaryDict([])

    @staticmethod
    def UpdateValue(
        value: _values.AFValue,
        update_mode: Data.AFUpdateOption,
        buffer_option: Data.AFBufferOption,
        /,
    ) -> None:
        pass
