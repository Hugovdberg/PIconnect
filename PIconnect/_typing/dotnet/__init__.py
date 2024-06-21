"""Mock for System.* classes."""

from typing import Protocol

from . import Data, Net, Security

__all__ = [
    "Data",
    "Exception",
    "Net",
    "Security",
    "TimeSpan",
]


class Exception:
    pass


class TimeSpan:
    def __init__(self, /, hours: int, minutes: int, seconds: int) -> None:
        self.Hours = hours
        self.Minutes = minutes
        self.Seconds = seconds


class DateTime(Protocol):
    """Mock for System.DateTime."""

    Year: int
    Month: int
    Day: int
    Hour: int
    Minute: int
    Second: int
    Millisecond: int
