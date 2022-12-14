from typing import Any, List

from . import Time


class AFValue:
    def __init__(
        self, value: Any, timestamp: Time.AFTime = Time.AFTime("MinValue")
    ) -> None:
        self.Value = value
        self.Timestamp = timestamp


class AFValues(List[AFValue]):
    def __init__(self):
        self.Count: int
        self.Value: AFValue
