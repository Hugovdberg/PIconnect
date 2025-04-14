"""The Search namespace provides query based searches."""

from collections.abc import Iterable
from typing import Generic, TypeVar

from .Asset import AFAttribute, AFElement
from .Database import AFDatabase
from .EventFrame import AFEventFrame

_AFSearchable = TypeVar(
    "_AFSearchable",
)


class AFSearch(Generic[_AFSearchable]):
    """Base class for AFSearch."""

    def __init__(self, database: AFDatabase, name: str, query: str) -> None:
        self.Database = database
        self.SearchName = name
        self.TokenCollection = query

    def GetTotalCount(self) -> int:
        """Return the total count of the search results."""
        return len(self.TokenCollection)

    def FindObjects(self) -> Iterable[_AFSearchable]:
        """Return the search results."""
        obs: list[_AFSearchable] = []
        for item in obs:
            yield item


class AFAttributeSearch(AFSearch[AFAttribute]):
    """Search for AF attributes."""


class AFElementSearch(AFSearch[AFElement]):
    """Search for AF elements."""


class AFEventFrameSearch(AFSearch[AFEventFrame]):
    """Search for AF elements."""
