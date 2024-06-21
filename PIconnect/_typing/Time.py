"""Mock classes for the AF.Time module."""

from typing import Optional

from . import dotnet as System


class AFTime:
    """Mock class of the AF.Time.AFTime class."""

    def __init__(self, time: str) -> None:
        self.UtcTime: System.DateTime

    Now: System.DateTime


class AFTimeRange:
    """Mock class of the AF.Time.AFTimeRange class."""

    def __init__(self, start_time: str, end_time: str):
        pass

    @staticmethod
    def Parse(start_time: str, end_time: str) -> "AFTimeRange":
        return AFTimeRange(start_time, end_time)


class AFTimeSpan:
    """Mock class of the AF.Time.AFTimeSpan class."""

    def __init__(self):
        pass

    @staticmethod
    def Parse(interval: Optional[str], /) -> "AFTimeSpan":
        """Stub for parsing strings that should return a AFTimeSpan."""
        return AFTimeSpan()
