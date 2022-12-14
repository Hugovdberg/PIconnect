from typing import Any, List, Optional, Union

from . import AF, Data, Generic, Time


class AFAttribute:
    def __init__(self, name: str) -> None:
        self.Name = name


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


AttributeDict = Generic.Dictionary[str, AFAttribute]
SummariesDict = Generic.Dictionary[Data.AFSummaryTypes, AFValues]
SummaryDict = Generic.Dictionary[Data.AFSummaryTypes, AFValue]
