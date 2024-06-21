"""Fake classes to mask SDK complexity."""

import dataclasses
import datetime
from typing import Any, Dict, Generic, Iterable, List, TypeVar

import pytest
import pytz

import PIconnect._typing.AF as AF
import PIconnect.PI as PI


@dataclasses.dataclass
class _UTCTime:
    Year: int
    Month: int
    Day: int
    Hour: int
    Minute: int
    Second: int
    Millisecond: int


class FakeAFTime(object):
    """Fake AFTime to mask away SDK complexity."""

    def __init__(self, timestamp: datetime.datetime):
        self.UtcTime = _UTCTime(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            timestamp.hour,
            timestamp.minute,
            timestamp.second,
            int(timestamp.microsecond / 1000),
        )


_a = TypeVar("_a")
_b = TypeVar("_b")


class FakeKeyValue(Generic[_a, _b]):
    """Container for fake Key:Value pairs."""

    def __init__(self, key: _a, value: _b) -> None:
        self.Key = key
        self.Value = value


class FakeAFValue(AF.Asset.AFValue, Generic[_a]):
    """Fake AFValue to mask away SDK complexity."""

    def __init__(self, value: _a, timestamp: datetime.datetime):
        self.Value = value
        self.Timestamp = FakeAFTime(timestamp)


class FakeAFValues(AF.Asset.AFValues, Generic[_a]):
    """Fake AFValues to mask away SDK complexity."""

    def __init__(self, values: Iterable[FakeAFValue[_a]]):
        self.Value = list(values)
        self.Count = len(self.Value)


class FakePIPoint_(Generic[_a]):
    """Fake PI Point to mask away SDK complexity."""

    def __init__(
        self,
        tag: str,
        values: Iterable[_a],
        timestamps: Iterable[datetime.datetime],
        attributes: Dict[str, Any],
    ):
        self.Name = tag
        self.values = [
            FakeAFValue(value, timestamp) for value, timestamp in zip(values, timestamps)
        ]
        self.attributes = [FakeKeyValue(*att) for att in attributes.items()]


class FakePIPoint(AF.PI.PIPoint, Generic[_a]):
    """Fake PI Point to mask away SDK complexity."""

    def __init__(self, pi_point: FakePIPoint_[_a]) -> None:
        self.pi_point = pi_point
        self.call_stack = ["%s created" % self.__class__.__name__]
        self.Name = pi_point.Name

    def CurrentValue(self) -> FakeAFValue[_a]:
        """Return the current value of the PI Point."""
        self.call_stack.append("CurrentValue called")
        return self.pi_point.values[-1]

    def LoadAttributes(self, *args: Any, **kwargs: Any) -> None:
        """Load the attributes of the PI Point."""
        self.call_stack.append("LoadAttributes called")

    def GetAttributes(self, *args: Any, **kwargs: Any) -> List[FakeKeyValue[str, Any]]:
        """Return the attributes of the PI Point."""
        self.call_stack.append("GetAttributes called")
        return self.pi_point.attributes

    def RecordedValues(self, *args: Any, **kwargs: Any) -> List[FakeAFValue[_a]]:
        """Return the recorded values of the PI Point."""
        self.call_stack.append("RecordedValues called")
        return self.pi_point.values

    def InterpolatedValues(self, *args: Any, **kwargs: Any) -> List[FakeAFValue[_a]]:
        """Return the interpolated values of the PI Point."""
        self.call_stack.append("InterpolatedValues called")
        return self.pi_point.values


class VirtualTestCase(object):
    """Test VirtualPIPoint addition."""

    def __init__(self):
        self.tag = "TEST_140_053_FQIS053_01_Meetwaarde"
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.timestamp_numbers = [
            1502654535.813,
            1502671554.038,
            1502695584.315,
            1502704569.874,
            1502709576.898,
            1502713512.168,
            1502718534.453,
            1502722585.816,
            1502731598.316,
            1502732545.013,
        ]
        self.timestamps = [
            datetime.datetime.fromtimestamp(x, tz=pytz.utc) for x in self.timestamp_numbers
        ]
        self.attributes = {"engunits": "m3/h", "descriptor": "Flow"}
        pi_point = FakePIPoint_(
            tag=self.tag,
            values=self.values,
            timestamps=self.timestamps,
            attributes=self.attributes,
        )
        self.point = PI.PIPoint(FakePIPoint(pi_point))


@pytest.fixture()
def pi_point() -> VirtualTestCase:
    """Return a VirtualTestCase object."""
    return VirtualTestCase()
