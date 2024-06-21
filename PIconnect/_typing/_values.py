"""Typing for AFValues and AFValue classes.

These classes are in a separate file to avoid circular imports.
"""

from typing import Any, List

from . import Time

_DEFAULT_TIME = Time.AFTime("MinValue")


class AFValue:
    def __init__(self, value: Any, timestamp: Time.AFTime = _DEFAULT_TIME) -> None:
        self.Value = value
        self.Timestamp = timestamp


class AFValues(List[AFValue]):
    def __init__(self):
        self.Count: int
        self.Value: List[AFValue]
