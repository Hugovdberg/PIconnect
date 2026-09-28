"""Mock classes for the System.Data module."""

from collections.abc import Iterator
from typing import Any

__all__ = [
    "DataRow",
    "DataRowCollection",
    "DataColumn",
    "DataColumnCollection",
    "DataTable",
]


class DataRow:
    __fields: dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        return self.__fields[key]


class DataRowCollection:
    rows: list[DataRow]

    def __iter__(self) -> Iterator[DataRow]:
        yield from self.rows


class DataColumn:
    def __init__(self, name: str) -> None:
        self.ColumnName = name


class DataColumnCollection:
    columns: list[DataColumn]

    def __iter__(self) -> Iterator[DataColumn]:
        yield from self.columns


class DataTable:
    Name: str
    Rows: list[DataRow]
    Columns: list[DataColumn]
