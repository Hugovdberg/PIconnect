"""Mock classes for the System.Data module."""

from typing import Any, Dict, Iterator, List

__all__ = [
    "DataRow",
    "DataRowCollection",
    "DataColumn",
    "DataColumnCollection",
    "DataTable",
]


class DataRow:
    __fields: Dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        return self.__fields[key]


class DataRowCollection:
    rows: List[DataRow]

    def __iter__(self) -> Iterator[DataRow]:
        yield from self.rows


class DataColumn:
    def __init__(self, name: str) -> None:
        self.ColumnName = name


class DataColumnCollection:
    columns: List[DataColumn]

    def __iter__(self) -> Iterator[DataColumn]:
        yield from self.columns


class DataTable:
    Name: str
    Rows: List[DataRow]
    Columns: List[DataColumn]
