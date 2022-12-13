from typing import Optional, Protocol


class DateTime(Protocol):
    """Mock for System.DateTime"""

    Year: int
    Month: int
    Day: int
    Hour: int
    Minute: int
    Second: int
    Millisecond: int


class AFTime:
    """Mock class of the AF.Time.AFTime class"""

    def __init__(self, time: str) -> None:
        self.UtcTime: DateTime


class AFTimeRange:
    """Mock class of the AF.Time.AFTimeRange class"""

    def __init__(self, start_time: str, end_time: str):
        pass


class AFTimeSpan:
    """Mock class of the AF.Time.AFTimeSpan class"""

    def __init__(self):
        pass

    @staticmethod
    def Parse(interval: Optional[str], /) -> "AFTimeSpan":
        """Stub for parsing strings that should return a AFTimeSpan"""
        return AFTimeSpan()
