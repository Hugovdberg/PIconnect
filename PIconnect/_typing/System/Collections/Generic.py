"""Contains interfaces and classes that define generic collections,
which allow users to create strongly typed collections that provide
better type safety and performance than non-generic strongly typed
collections.
"""

from collections.abc import Iterable
from typing import Generic, Protocol, TypeVar

__all__ = ["Dictionary", "KeyValuePair"]

TKey = TypeVar("TKey", covariant=True)
TValue = TypeVar("TValue", covariant=True)


class Dictionary(Protocol[TKey, TValue]):
    """Represents a collection of keys and values."""

    def __init__(self, items: Iterable[tuple[TKey, TValue]] | None = None, /) -> None:
        """Initializes a new instance of the Dictionary class that contains elements copied from the specified IDictionary and uses the default equality comparer for the key type."""
        ...


class KeyValuePair(Generic[TKey, TValue]):
    """Represents a key/value pair that can be set or retrieved."""

    def __init__(self, key: TKey, value: TValue, /) -> None:
        self.Key = key
        self.Value = value
