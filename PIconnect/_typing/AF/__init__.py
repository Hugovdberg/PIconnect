"""Mock classes for the AF namespace of the OSIsoft PI-AF SDK."""

from collections.abc import Iterator

from . import PI, Asset, Data, EventFrame, Search, Time, UnitsOfMeasure
from .Database import AFDatabase

__all__ = [
    "Asset",
    "Data",
    "EventFrame",
    "PI",
    "Search",
    "Time",
    "UnitsOfMeasure",
    "AFDatabase",
    "AFCategory",
    "PISystem",
    "PISystems",
]


class AFCategory:
    """Mock class of the AF.AFCategory class."""


class AFCategories(list[AFCategory]):
    def __init__(self, elements: list[AFCategory]) -> None:
        self.Count: int
        self._values = elements


class PISystem:
    """Mock class of the AF.PISystem class."""

    class InternalDatabases:
        """Mock class for the AF.PISystem.Databases property."""

        def __init__(self) -> None:
            self.DefaultDatabase: AFDatabase | None = AFDatabase("TestDatabase")

        def __iter__(self) -> Iterator[AFDatabase]:
            if self.DefaultDatabase is not None:
                yield from [self.DefaultDatabase]

        def __getitem__(self, name: str) -> AFDatabase | None:
            """Return the AFDatabase with the given name."""
            if self.DefaultDatabase and name == self.DefaultDatabase.Name:
                return self.DefaultDatabase

    def __init__(self, name: str) -> None:
        self.Name = name
        self.Databases = PISystem.InternalDatabases()
        self._connected = False

    def Connect(self) -> None:
        """Stub to connect to the testing system."""
        self._connected = True

    def Disconnect(self) -> None:
        """Stub to disconnect from the testing system."""
        self._connected = False


class PISystems:
    """Mock class of the AF.PISystems class."""

    Version = "0.0.0.0"

    def __init__(self) -> None:
        self.DefaultPISystem = PISystem("TestingAF")
        self.Count = 1

    def __iter__(self) -> Iterator[PISystem]:
        return (x for x in [self.DefaultPISystem])

    def __getitem__(self, name: str) -> PISystem | None:
        """Return the PISystem with the given name."""
        if name == self.DefaultPISystem.Name:
            return self.DefaultPISystem
