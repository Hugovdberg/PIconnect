from typing import List, Optional, Union

from . import AF, Data, Generic
from . import UnitsOfMeasure as UOM
from ._values import AFValue, AFValues

__all__ = [
    "AFAttribute",
    "AFAttributes",
    "AFBaseElement",
    "AFElement",
    "AFElements",
    "AFElementTemplate",
    "AFValue",
    "AFValues",
]


class AFAttribute:
    def __init__(self, name: str) -> None:
        self.Attributes: AFAttributes
        self.Data: Data.AFData
        self.Description: str
        self.DefaultUOM: UOM.UOM
        self.Name = name
        self.Parent: Optional[AFAttribute]

    @staticmethod
    def GetValue() -> AFValue:
        """Stub for getting a value"""
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
    """Mock class of the AF.AFElement class"""


class AFElements(List[AFElement]):
    def __init__(self, elements: List[AFElement]) -> None:
        self.Count: int
        self._values = elements

    def get_Item(self, name: Union[str, int]) -> AFElement:
        """Stub for the indexer"""
        if isinstance(name, int):
            return self._values[name]
        return AFElement(name)


class AFElementTemplate:
    """Mock class of the AF.Asset.AFElementTemplate class"""


AttributeDict = Generic.Dictionary[str, AFAttribute]
