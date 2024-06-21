"""Mock classes for the AF namespace of the OSIsoft PI-AF SDK."""

from typing import Iterator, List

from . import PI, Asset, Data, EventFrame, Time, UnitsOfMeasure

__all__ = [
    "Asset",
    "Data",
    "EventFrame",
    "PI",
    "Time",
    "UnitsOfMeasure",
    "AFDatabase",
    "AFCategory",
    "PISystem",
    "PISystems",
]


class AFCategory:
    """Mock class of the AF.AFCategory class."""


class AFCategories(List[AFCategory]):
    def __init__(self, elements: List[AFCategory]) -> None:
        self.Count: int
        self._values = elements


class AFDatabase:
    """Mock class of the AF.AFDatabase class."""

    def __init__(self, name: str) -> None:
        self.Name = name
        self.Elements = Asset.AFElements([Asset.AFElement("TestElement")])
        self.Tables = Asset.AFTables([Asset.AFTable("TestTable")])


class PISystem:
    """Mock class of the AF.PISystem class."""

    class InternalDatabases:
        """Mock class for the AF.PISystem.Databases property."""

        def __init__(self) -> None:
            self.DefaultDatabase = AFDatabase("TestDatabase")

        def __iter__(self) -> Iterator[AFDatabase]:
            return (x for x in [self.DefaultDatabase])

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

    def __iter__(self) -> Iterator[PISystem]:
        return (x for x in [self.DefaultPISystem])
