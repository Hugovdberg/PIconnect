from typing import Any, Generic, Iterable, Iterator, Tuple, TypeVar

from . import Asset, Data

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DictItem(Generic[_KT, _VT]):
    def __init__(self, key: _KT, value: _VT) -> None:
        self.Key = key
        self.Value = value


class Dictionary(Generic[_KT, _VT]):
    def __init__(self, items: Iterable[Tuple[_KT, _VT]]) -> None:
        self.Items = items

    def __iter__(self) -> Iterator[DictItem[_KT, _VT]]:
        for item in self.Items:
            yield DictItem(*item)


AttributeDict = Dictionary[str, Asset.AFAttribute]
PropertyDict = Dictionary[str, Any]
SummariesDict = Dictionary[Data.AFSummaryTypes, Asset.AFValues]
SummaryDict = Dictionary[Data.AFSummaryTypes, Asset.AFValue]
