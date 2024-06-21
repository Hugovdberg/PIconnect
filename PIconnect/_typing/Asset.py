"""Mock classes for the AF module."""

from typing import List, Optional, Union

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
    def __init__(self, name: str) -> None:
        self.Attributes: AFAttributes
        self.Data: Data.AFData
        self.DataReference: AFDataReference
        self.Description: str
        self.DefaultUOM: UOM.UOM
        self.Name = name
        self.Parent: Optional[AFAttribute]

    @staticmethod
    def GetValue() -> AFValue:
        """Stub for getting a value."""
        return AFValue(0)


class AFAttributes(List[AFAttribute]):
    def __init__(self, elements: List[AFAttribute]) -> None:
        self.Count: int
        self._values = elements


class AFBaseElement:
    def __init__(self, name: str, parent: Optional["AFElement"] = None) -> None:
        self.Attributes: AFAttributes
        self.Categories: AF.AFCategories
        self.Description: str
        self.Elements: AFElements
        self.Name = name
        self.Parent = parent


class AFElement(AFBaseElement):
    """Mock class of the AF.AFElement class."""


class AFElements(List[AFElement]):
    def __init__(self, elements: List[AFElement]) -> None:
        self.Count: int
        self._values = elements

    def get_Item(self, name: Union[str, int]) -> AFElement:
        """Stub for the indexer."""
        if isinstance(name, int):
            return self._values[name]
        return AFElement(name)


class AFElementTemplate:
    """Mock class of the AF.Asset.AFElementTemplate class."""


class AFDataReference:
    from . import PI

    def __init__(
        self, name: str, attribute: AFAttribute, pi_point: Optional[PI.PIPoint] = None
    ) -> None:
        self.Attribute = attribute
        self.Name = name
        self.PIPoint = pi_point


class AFTable:
    def __init__(self, name: str) -> None:
        self.Name = name
        self.Table: System.Data.DataTable


class AFTables(List[AFTable]):
    def __init__(self, elements: List[AFTable]) -> None:
        self.Count: int
        self._values = elements


AttributeDict = Generic.Dictionary[str, AFAttribute]
