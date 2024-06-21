"""Mocking the Generic types from System.Collections.Generic namespace.

TODO: Migrate to the `_typing.dotnet` module.
"""

from typing import Any, Generic, Iterable, Iterator, Optional, Tuple, TypeVar

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


class TimeSpan:
    def __init__(self, hours: int, minutes: int, seconds: int) -> None:
        self.Hours = hours
        self.Minutes = minutes
        self.Seconds = seconds


class SecureString:
    def __init__(self) -> None:
        self.Value = ""

    def AppendChar(self, char: str) -> None:
        self.Value += char


class NetworkCredential:
    def __init__(
        self, username: str, password: SecureString, domain: Optional[str] = None
    ) -> None:
        self.UserName = username
        self.Password = password
        self.Domain = domain


PropertyDict = Dictionary[str, Any]
