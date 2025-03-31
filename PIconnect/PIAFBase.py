"""Base element class for PI AF elements."""

from collections.abc import Iterator, Sequence
from typing import Generic, Self, TypeVar, overload

import pandas as pd  # type: ignore

import PIconnect.AFSDK as SDK
import PIconnect.PIAFAttribute as PIattr
from PIconnect.AFSDK import System

ElementType = TypeVar("ElementType", bound=SDK.AF.Asset.AFBaseElement)


class PIAFBaseElement(Generic[ElementType]):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, element: ElementType) -> None:
        self.element = element

    def __repr__(self) -> str:
        """Return the string representation of the element."""
        return f"{self.__class__.__qualname__}({self.name})"

    @property
    def name(self) -> str:
        """Return the name of the current element."""
        return self.element.Name

    @property
    def attributes(self) -> dict[str, PIattr.PIAFAttribute]:
        """Return a dictionary of the attributes of the current element."""
        return {a.Name: PIattr.PIAFAttribute(a) for a in self.element.Attributes}

    @property
    def categories(self) -> SDK.AF.AFCategories:
        """Return the categories of the current element."""
        return self.element.Categories

    @property
    def description(self) -> str:
        """Return the description of the current element."""
        return self.element.Description


class PIAFElement(PIAFBaseElement[SDK.AF.Asset.AFElement]):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    @property
    def parent(self) -> "PIAFElement | None":
        """Return the parent element of the current element, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self) -> dict[str, "PIAFElement"]:
        """Return a dictionary of the direct child elements of the current element."""
        return {c.Name: self.__class__(c) for c in self.element.Elements}

    def descendant(self, path: str) -> "PIAFElement":
        """Return a descendant of the current element from an exact path."""
        return self.__class__(self.element.Elements.get_Item(path))


class PIAFElementList(Sequence[PIAFElement]):
    """Container for a list of PIAFElement objects."""

    def __init__(self, elements: list[PIAFElement]) -> None:
        self._elements = elements

    @overload
    def __getitem__(self, index: int) -> PIAFElement: ...
    @overload
    def __getitem__(self, index: slice) -> Self: ...
    def __getitem__(self, index: int | slice) -> PIAFElement | Self:
        """Return the element at the specified index."""
        if isinstance(index, slice):
            return self.__class__(self._elements[index])
        return self._elements[index]

    def __len__(self) -> int:
        """Return the number of elements in the list."""
        return len(self._elements)

    def __iter__(self) -> Iterator[PIAFElement]:
        """Return an iterator over the elements in the list."""
        yield from self._elements


class PIAFEventFrame(PIAFBaseElement[SDK.AF.EventFrame.AFEventFrame]):
    """Container for PI AF Event Frames in the database."""

    version = "0.1.0"

    @property
    def event_frame(self) -> SDK.AF.EventFrame.AFEventFrame:
        """Return the underlying AF Event Frame object."""
        return self.element

    @property
    def parent(self) -> "PIAFEventFrame | None":
        """Return the parent element of the current event frame, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self) -> dict[str, "PIAFEventFrame"]:
        """Return a dictionary of the direct child event frames of the current event frame."""
        return {c.Name: self.__class__(c) for c in self.element.EventFrames}


class PIAFTable:
    """Container for PI AF Tables in the database."""

    def __init__(self, table: SDK.AF.Asset.AFTable) -> None:
        self._table = table

    @property
    def columns(self) -> list[str]:
        """Return the names of the columns in the table."""
        return [col.ColumnName for col in self._table.Table.Columns]

    @property
    def _rows(self) -> list[System.Data.DataRow]:
        return self._table.Table.Rows

    @property
    def name(self) -> str:
        """Return the name of the table."""
        return self._table.Name

    @property
    def shape(self) -> tuple[int, int]:
        """Return the shape of the table."""
        return (len(self._rows), len(self.columns))

    @property
    def data(self) -> pd.DataFrame:
        """Return the data in the table as a pandas DataFrame."""
        return pd.DataFrame([{col: row[col] for col in self.columns} for row in self._rows])
