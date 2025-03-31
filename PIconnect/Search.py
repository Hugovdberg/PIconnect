"""Search the AF database for different objects."""

import abc
import warnings
from collections.abc import Iterator, Sequence
from typing import Generic, TypeVar

import PIconnect.AFSDK as SDK

from . import Asset

SearchResultType = TypeVar(
    "SearchResultType",
    # PIAFBase.PIAFElement,
    # PIAFBase.PIAFEventFrame,
    # PIAFAttribute.PIAFAttribute,
)
AFSearchResultType = TypeVar("AFSearchResultType", covariant=True)


class SearchResult(Generic[AFSearchResultType, SearchResultType], abc.ABC):
    """Container for search results."""

    def __init__(
        self,
        search: "SDK.AF.Search.AFSearch[AFSearchResultType]",
    ) -> None:
        self.search = search
        self.result_type: type[SearchResultType]

    @property
    def name(self) -> str:
        """Return the name of the search result."""
        return self.search.SearchName

    @property
    def count(self) -> int:
        """Return the number of items in the search result."""
        return self.search.GetTotalCount()

    def __iter__(self) -> Iterator[SearchResultType]:
        """Return an iterator over the items in the search result."""
        for item in self.search.FindObjects():
            yield self.result_type(item)  # type: ignore

    def one(self) -> SearchResultType:
        """Return the only item in the search result.

        Raises
        ------
            ValueError: If there are no results or more than one result.
        """
        if self.count == 0:
            raise ValueError("No results found")
        if self.count > 1:
            raise ValueError(f"More than one result found ({self.count} results)")
        return next(iter(self))

    @abc.abstractmethod
    def to_list(self) -> Sequence[SearchResultType]:
        """Return all items in the search result in a sequence."""
        pass


class AttributeSearchResult(SearchResult[SDK.AF.Asset.AFAttribute, Asset.AFAttribute]):
    """Container for attribute search results."""

    def __init__(
        self,
        search: SDK.AF.Search.AFAttributeSearch,
    ) -> None:
        super().__init__(search)
        self.result_type = Asset.AFAttribute

    def to_list(self) -> Asset.AFAttributeList:
        """Return all items in the search result."""
        return Asset.AFAttributeList(list(self))


class ElementSearchResult(SearchResult[SDK.AF.Asset.AFElement, Asset.AFElement]):
    """Container for attribute search results."""

    def __init__(
        self,
        search: SDK.AF.Search.AFElementSearch,
    ) -> None:
        super().__init__(search)
        self.result_type = Asset.AFElement

    def to_list(self) -> Asset.AFElementList:
        """Return all items in the search result."""
        return Asset.AFElementList(list(self))


class Search:
    """Search the AF database for different objects."""

    def __init__(self, database: SDK.AF.AFDatabase) -> None:
        self.database = database

    def attributes(
        self, query: str, query_name: str = "element_search"
    ) -> AttributeSearchResult:
        """Search for elements in the AF database."""
        search = SDK.AF.Search.AFAttributeSearch(self.database, query_name, query)
        return AttributeSearchResult(search)

    def elements(self, query: str, query_name: str = "element_search") -> ElementSearchResult:
        """Search for elements in the AF database."""
        search = SDK.AF.Search.AFElementSearch(self.database, query_name, query)
        return ElementSearchResult(search)

    def _descendant(self, path: str) -> Asset.AFElement:
        return Asset.AFElement(self.database.Elements.get_Item(path))

    def __call__(self, query: str | list[str]) -> Asset.AFAttributeList:
        """Search AFAttributes by element|attribute path strings.

        Return a list of AFAttributes directly from a list of element|attribute path strings

            like this:

        list("BaseElement/childElement/childElement|Attribute|ChildAttribute|ChildAttribute",
        "BaseElement/childElement/childElement|Attribute|ChildAttribute|ChildAttribute")

        """
        warnings.warn(
            """Call to Search.__call__ is deprecated, use Search.<element_type> instead""",
            DeprecationWarning,
            stacklevel=2,
        )
        attributelist = Asset.AFAttributeList([])
        if isinstance(query, list):
            for x in query:
                attributelist.extend(self(x))
            return attributelist
        if "|" in query:
            splitpath = query.split("|")
            elem = self._descendant(splitpath[0])
            attribute = elem.attributes[splitpath[1]]
            if len(splitpath) > 2:
                for x in range(len(splitpath) - 2):
                    attribute = attribute.children[splitpath[x + 2]]
            attributelist.append(attribute)
        return attributelist
