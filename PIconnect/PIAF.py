"""PIAF - Core containers for connections to the PI Asset Framework."""

import dataclasses
import warnings
from typing import Any, cast

import PIconnect.AFSDK as SDK
from PIconnect import PIAFBase, PIConsts, Search, Time
from PIconnect._utils import InitialisationWarning
from PIconnect.AFSDK import System

_DEFAULT_EVENTFRAME_SEARCH_MODE = PIConsts.EventFrameSearchMode.STARTING_AFTER


@dataclasses.dataclass(frozen=True)
class PIAFServer:
    """Reference to a PI AF server and its databases."""

    server: SDK.AF.PISystem
    databases: dict[str, SDK.AF.AFDatabase] = dataclasses.field(default_factory=dict)

    def __getitem__(self, attr: str) -> SDK.AF.PISystem | dict[str, SDK.AF.AFDatabase]:
        """Allow access to attributes as if they were dictionary items."""
        return getattr(self, attr)


ServerSpec = dict[str, SDK.AF.PISystem | dict[str, SDK.AF.AFDatabase]]


def _lookup_servers() -> dict[str, ServerSpec]:
    servers: dict[str, PIAFServer] = {}
    for s in SDK.AF.PISystems():
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


def _lookup_default_server() -> ServerSpec | None:
    servers = _lookup_servers()
    if SDK.AF.PISystems().DefaultPISystem:
        return servers[SDK.AF.PISystems().DefaultPISystem.Name]
    elif len(servers) > 0:
        return servers[list(_lookup_servers())[0]]
    else:
        return None


class PIAFDatabase:
    """Context manager for connections to the PI Asset Framework database."""

    version = "0.3.0"

    servers: dict[str, ServerSpec] = _lookup_servers()
    default_server: ServerSpec | None = _lookup_default_server()

    def __init__(self, server: str | None = None, database: str | None = None) -> None:
        server_spec = self._initialise_server(server)
        self.server: SDK.AF.PISystem = server_spec["server"]  # type: ignore
        self.database: SDK.AF.AFDatabase = self._initialise_database(server_spec, database)
        self.search = Search.Search(self.database)

    def _initialise_server(self, server: str | None) -> ServerSpec:
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
        self, server: ServerSpec, database: str | None
    ) -> SDK.AF.AFDatabase:
        def default_db():
            default = self.server.Databases.DefaultDatabase
            if default is None:
                raise ValueError("No database specified and no default database found.")
            return default

        if database is None:
            return default_db()

        databases = cast(dict[str, SDK.AF.AFDatabase], server["databases"])
        if database not in databases:
            message = 'Database "{database}" not found, using the default database.'
            warnings.warn(
                message=message.format(database=database), category=UserWarning, stacklevel=2
            )
            return default_db()

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
    def children(self) -> dict[str, PIAFBase.PIAFElement]:
        """Return a dictionary of the direct child elements of the database."""
        return {c.Name: PIAFBase.PIAFElement(c) for c in self.database.Elements}

    @property
    def tables(self) -> dict[str, PIAFBase.PIAFTable]:
        """Return a dictionary of the tables in the database."""
        return {t.Name: PIAFBase.PIAFTable(t) for t in self.database.Tables}

    def descendant(self, path: str) -> PIAFBase.PIAFElement:
        """Return a descendant of the database from an exact path."""
        return PIAFBase.PIAFElement(self.database.Elements.get_Item(path))

    def event_frames(
        self,
        start_time: Time.TimeLike = "",
        start_index: int = 0,
        max_count: int = 1000,
        search_mode: PIConsts.EventFrameSearchMode = _DEFAULT_EVENTFRAME_SEARCH_MODE,
        search_full_hierarchy: bool = False,
    ) -> dict[str, PIAFBase.PIAFEventFrame]:
        """Search for event frames in the database."""
        _start_time = Time.to_af_time(start_time)
        _search_mode = SDK.AF.EventFrame.AFEventFrameSearchMode(int(search_mode))
        return {
            frame.Name: PIAFBase.PIAFEventFrame(frame)
            for frame in SDK.AF.EventFrame.AFEventFrame.FindEventFrames(
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
