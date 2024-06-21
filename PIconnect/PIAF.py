"""PIAF - Core containers for connections to the PI Asset Framework."""

import dataclasses
import warnings
from typing import Any, Dict, List, Optional, Union, cast

import pandas as pd

from PIconnect import AF, PIAFAttribute, PIAFBase, PIConsts, _time
from PIconnect._utils import InitialisationWarning
from PIconnect.AFSDK import System

_DEFAULT_EVENTFRAME_SEARCH_MODE = PIConsts.EventFrameSearchMode.STARTING_AFTER


@dataclasses.dataclass(frozen=True)
class PIAFServer:
    """Reference to a PI AF server and its databases."""

    server: AF.PISystem
    databases: Dict[str, AF.AFDatabase] = dataclasses.field(default_factory=dict)

    def __getitem__(self, attr: str) -> Union[AF.PISystem, Dict[str, AF.AFDatabase]]:
        """Allow access to attributes as if they were dictionary items."""
        return getattr(self, attr)


ServerSpec = Dict[str, Union[AF.PISystem, Dict[str, AF.AFDatabase]]]


def _lookup_servers() -> Dict[str, ServerSpec]:
    servers: Dict[str, PIAFServer] = {}
    for s in AF.PISystems():
        try:
            servers[s.Name] = server = PIAFServer(s)
            for d in s.Databases:
                try:
                    server.databases[d.Name] = d
                except (Exception, System.Exception) as e:  # type: ignore
                    warnings.warn(
                        f"Failed loading database data for {d.Name} on {s.Name} "
                        f"with error {type(cast(Exception, e)).__qualname__}",
                        InitialisationWarning,
                        stacklevel=2,
                    )
        except (Exception, System.Exception) as e:  # type: ignore
            warnings.warn(
                f"Failed loading server data for {s.Name} "
                f"with error {type(cast(Exception, e)).__qualname__}",
                InitialisationWarning,
                stacklevel=2,
            )
    return {
        server_name: {
            "server": server.server,
            "databases": dict(server.databases.items()),
        }
        for server_name, server in servers.items()
    }


def _lookup_default_server() -> Optional[ServerSpec]:
    servers = _lookup_servers()
    if AF.PISystems().DefaultPISystem:
        return servers[AF.PISystems().DefaultPISystem.Name]
    elif len(servers) > 0:
        return servers[list(_lookup_servers())[0]]
    else:
        return None


class PIAFDatabase(object):
    """Context manager for connections to the PI Asset Framework database."""

    version = "0.3.0"

    servers: Dict[str, ServerSpec] = _lookup_servers()
    default_server: Optional[ServerSpec] = _lookup_default_server()

    def __init__(self, server: Optional[str] = None, database: Optional[str] = None) -> None:
        server_spec = self._initialise_server(server)
        self.server: AF.PISystem = server_spec["server"]  # type: ignore
        self.database: AF.AFDatabase = self._initialise_database(server_spec, database)

    def _initialise_server(self, server: Optional[str]) -> ServerSpec:
        if server is None:
            if self.default_server is None:
                raise ValueError("No server specified and no default server found.")
            return self.default_server

        if server not in self.servers:
            if self.default_server is None:
                raise ValueError(f'Server "{server}" not found and no default server found.')
            message = 'Server "{server}" not found, using the default server.'
            warnings.warn(
                message=message.format(server=server), category=UserWarning, stacklevel=2
            )
            return self.default_server

        return self.servers[server]

    def _initialise_database(
        self, server: ServerSpec, database: Optional[str]
    ) -> AF.AFDatabase:
        default_db = self.server.Databases.DefaultDatabase
        if database is None:
            return default_db

        databases = cast(Dict[str, AF.AFDatabase], server["databases"])
        if database not in databases:
            message = 'Database "{database}" not found, using the default database.'
            warnings.warn(
                message=message.format(database=database), category=UserWarning, stacklevel=2
            )
            return default_db

        return databases[database]

    def __enter__(self) -> "PIAFDatabase":
        """Open the PI AF server connection context."""
        self.server.Connect()
        return self

    def __exit__(self, *args: Any) -> None:
        """Close the PI AF server connection context."""
        pass
        # Disabled disconnecting because garbage collection sometimes impedes
        # connecting to another server later
        # self.server.Disconnect()

    def __repr__(self) -> str:
        """Return a representation of the PI AF database connection."""
        return f"{self.__class__.__qualname__}(\\\\{self.server_name}\\{self.database_name})"

    @property
    def server_name(self) -> str:
        """Return the name of the connected PI AF server."""
        return self.server.Name

    @property
    def database_name(self) -> str:
        """Return the name of the connected PI AF database."""
        return self.database.Name

    @property
    def children(self) -> Dict[str, "PIAFElement"]:
        """Return a dictionary of the direct child elements of the database."""
        return {c.Name: PIAFElement(c) for c in self.database.Elements}

    @property
    def tables(self) -> Dict[str, "PIAFTable"]:
        """Return a dictionary of the tables in the database."""
        return {t.Name: PIAFTable(t) for t in self.database.Tables}

    def descendant(self, path: str) -> "PIAFElement":
        """Return a descendant of the database from an exact path."""
        return PIAFElement(self.database.Elements.get_Item(path))

    def search(self, query: Union[str, List[str]]) -> List[PIAFAttribute.PIAFAttribute]:
        """Search PIAFAttributes by element|attribute path strings.

        Return a list of PIAFAttributes directly from a list of element|attribute path strings

            like this:

        list("BaseElement/childElement/childElement|Attribute|ChildAttribute|ChildAttribute",
        "BaseElement/childElement/childElement|Attribute|ChildAttribute|ChildAttribute")

        """
        attributelist: List[PIAFAttribute.PIAFAttribute] = []
        if isinstance(query, List):
            return [y for x in query for y in self.search(x)]
        if "|" in query:
            splitpath = query.split("|")
            elem = self.descendant(splitpath[0])
            attribute = elem.attributes[splitpath[1]]
            if len(splitpath) > 2:
                for x in range(len(splitpath) - 2):
                    attribute = attribute.children[splitpath[x + 2]]
                attributelist.append(attribute)
        return attributelist

    def event_frames(
        self,
        start_time: _time.TimeLike = "",
        start_index: int = 0,
        max_count: int = 1000,
        search_mode: PIConsts.EventFrameSearchMode = _DEFAULT_EVENTFRAME_SEARCH_MODE,
        search_full_hierarchy: bool = False,
    ) -> Dict[str, "PIAFEventFrame"]:
        """Search for event frames in the database."""
        _start_time = _time.to_af_time(start_time)
        _search_mode = AF.EventFrame.AFEventFrameSearchMode(int(search_mode))
        return {
            frame.Name: PIAFEventFrame(frame)
            for frame in AF.EventFrame.AFEventFrame.FindEventFrames(
                self.database,
                None,
                _start_time,
                start_index,
                max_count,
                _search_mode,
                None,
                None,
                None,
                None,
                search_full_hierarchy,
            )
        }


class PIAFElement(PIAFBase.PIAFBaseElement[AF.Asset.AFElement]):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    @property
    def parent(self) -> Optional["PIAFElement"]:
        """Return the parent element of the current element, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self) -> Dict[str, "PIAFElement"]:
        """Return a dictionary of the direct child elements of the current element."""
        return {c.Name: self.__class__(c) for c in self.element.Elements}

    def descendant(self, path: str) -> "PIAFElement":
        """Return a descendant of the current element from an exact path."""
        return self.__class__(self.element.Elements.get_Item(path))


class PIAFEventFrame(PIAFBase.PIAFBaseElement[AF.EventFrame.AFEventFrame]):
    """Container for PI AF Event Frames in the database."""

    version = "0.1.0"

    @property
    def event_frame(self) -> AF.EventFrame.AFEventFrame:
        """Return the underlying AF Event Frame object."""
        return self.element

    @property
    def parent(self) -> Optional["PIAFEventFrame"]:
        """Return the parent element of the current event frame, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self) -> Dict[str, "PIAFEventFrame"]:
        """Return a dictionary of the direct child event frames of the current event frame."""
        return {c.Name: self.__class__(c) for c in self.element.EventFrames}


class PIAFTable:
    """Container for PI AF Tables in the database."""

    def __init__(self, table: AF.Asset.AFTable) -> None:
        self._table = table

    @property
    def columns(self) -> List[str]:
        """Return the names of the columns in the table."""
        return [col.ColumnName for col in self._table.Table.Columns]

    @property
    def _rows(self) -> List[System.Data.DataRow]:
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
