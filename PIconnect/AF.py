"""Generics for AF collections."""

from collections.abc import Iterable, Iterator, MutableSequence
from typing import Protocol, Self, TypeVar, overload


class NamedItem(Protocol):
    """Protocol for an item with a name."""

    @property
    def name(self) -> str:
        """Return the name of the item."""
        ...


NamedItemType = TypeVar("NamedItemType", bound=NamedItem)


class NamedItemList(MutableSequence[NamedItemType]):
    """A list of items with names.

    This class provides a way to access items by index or by name.
    """

    def __init__(self, elements: MutableSequence[NamedItemType]) -> None:
        self._elements = elements

    @overload
    def __getitem__(self, index: int | str) -> NamedItemType: ...
    @overload
    def __getitem__(self, index: slice) -> Self: ...
    def __getitem__(self, index: int | str | slice) -> NamedItemType | Self:
        """Return the list item at the given index or the list item with the given name."""
        match index:
            case int():
                return self._elements[index]
            case str():
                for attr in self._elements:
                    if attr.name == index:
                        return attr
                raise KeyError(f"List item {index} not found.")
            case slice():
                return self.__class__(self._elements[index])
            case _:
                raise TypeError("Index must be an int, string or slice of int.")  # type: ignore

    def __len__(self) -> int:
        """Return the number of items in the list."""
        return len(self._elements)

    def __iter__(self) -> Iterator[NamedItemType]:
        """Return an iterator over the items in the list."""
        return iter(self._elements)

    @overload
    def __setitem__(self, index: int | str, value: NamedItemType) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[NamedItemType]) -> None: ...
    def __setitem__(
        self, index: int | str | slice, value: NamedItemType | Iterable[NamedItemType]
    ) -> None:
        """Set the list item at the given index or the list item with the given name."""
        match index:
            case int():
                self._elements[index] = value  # type: ignore
            case str():
                for i, attr in enumerate(self._elements):
                    if attr.name == index:
                        self._elements[i] = value  # type: ignore
                        return
                raise KeyError(f"List item {index} not found.")
            case slice():
                if isinstance(value, Iterable):
                    self._elements[index] = list(value)
                else:
                    raise TypeError("Value must be an iterable.")
            case _:
                raise TypeError("Index must be an int or string.")  # type: ignore

    def __delitem__(self, index: int | str | slice) -> None:
        """Delete the list item at the given index or the list item with the given name."""
        match index:
            case int():
                del self._elements[index]
            case slice():
                del self._elements[index]
            case str():
                for i, attr in enumerate(self._elements):
                    if attr.name == index:
                        del self._elements[i]
                        return
                raise KeyError(f"List item {index} not found.")
            case _:
                raise TypeError("Index must be an int or string.")  # type: ignore

    def insert(self, index: int, value: NamedItemType) -> None:
        """Insert a new item at the given index."""
        self._elements.insert(index, value)

    def append(self, value: NamedItemType) -> None:
        """Append a new item to the end of the list."""
        self._elements.append(value)

    def extend(self, values: Iterable[NamedItemType]) -> None:
        """Extend the list with a new iterable of items."""
        self._elements.extend(values)

    def __reversed__(self) -> Iterator[NamedItemType]:
        """Return a reverse iterator over the items in the list."""
        return reversed(self._elements)

    def __repr__(self) -> str:
        """Return the string representation of the list."""
        return f"{self.__class__.__qualname__}({len(self._elements)} items)"
