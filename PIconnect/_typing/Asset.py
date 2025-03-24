"""Mock classes for the AF module."""

from collections.abc import Iterator
from typing import cast

from . import AF, Data, Generic
from . import UnitsOfMeasure as UOM
from . import dotnet as System
from ._values import AFValue, AFValues

__all__ = [
    "AFAttribute",
    "AFAttributes",
    "AFBaseElement",
    "AFElement",
    "AFElements",
    "AFElementTemplate",
    "AFTable",
    "AFTables",
    "AFValue",
    "AFValues",
]


class AFAttribute:
    def __init__(self, name: str, parent: "AFAttribute | None" = None) -> None:
        self.Attributes: AFAttributes
        if parent is None:
            self.Attributes = AFAttributes(
                [
                    AFAttribute("Attribute1", parent=self),
                    AFAttribute("Attribute2", parent=self),
                ]
            )
        self.Data: Data.AFData
        self.DataReference: AFDataReference
        self.Description: str = f"Description of {name}"
        self.DefaultUOM = UOM.UOM()
        self.Name = name
        self.Parent = parent

    @staticmethod
    def GetValue() -> AFValue:
        """Stub for getting a value."""
        return AFValue(0)


class AFAttributes(list[AFAttribute]):
    def __init__(self, elements: list[AFAttribute]) -> None:
        self.Count: int
        self._values = elements

    def __iter__(self) -> Iterator[AFAttribute]:
        yield from self._values


class AFBaseElement:
    def __init__(self, name: str, parent: "AFElement | None" = None) -> None:
        self.Attributes = AFAttributes(
            [
                AFAttribute("Attribute1"),
                AFAttribute("Attribute2"),
            ]
        )
        self.Categories: AF.AFCategories
        self.Description: str
        self.Elements: AFElements
        if parent is None:
            self.Elements = AFElements(
                [
                    AFElement("Element1", parent=cast(AFElement, self)),
                    AFElement("Element2", parent=cast(AFElement, self)),
                    AFElement("BaseElement", parent=cast(AFElement, self)),
                ]
            )
        self.Name = name
        self.Parent = parent


class AFElement(AFBaseElement):
    """Mock class of the AF.AFElement class."""


class AFElements(list[AFElement]):
    def __init__(self, elements: list[AFElement]) -> None:
        self.Count: int
        self._values = elements

    def get_Item(self, name: str | int) -> AFElement:
        """Stub for the indexer."""
        if isinstance(name, int):
            return self._values[name]
        return AFElement(name)

    def __iter__(self) -> Iterator[AFElement]:
        yield from self._values


class AFElementTemplate:
    """Mock class of the AF.Asset.AFElementTemplate class."""


class AFDataReference:
    from . import PI

    def __init__(
        self, name: str, attribute: AFAttribute, pi_point: PI.PIPoint | None = None
    ) -> None:
        self.Attribute = attribute
        self.Name = name
        self.PIPoint = pi_point


class AFTable:
    def __init__(self, name: str) -> None:
        self.Name = name
        self.Table: System.Data.DataTable


class AFTables(list[AFTable]):
    def __init__(self, elements: list[AFTable]) -> None:
        self.Count: int
        self._values = elements


AttributeDict = Generic.Dictionary[str, AFAttribute]
