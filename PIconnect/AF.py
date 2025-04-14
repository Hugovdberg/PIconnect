"""AF - Core containers for connections to the PI Asset Framework."""

import logging
import warnings
from typing import Any, Self

from PIconnect import Asset, EventFrame, Search, Time, dotnet

_logger = logging.getLogger(__name__)
_DEFAULT_EVENTFRAME_SEARCH_MODE = EventFrame.EventFrameSearchMode.STARTING_AFTER


class AFDatabase:
    """Context manager for connections to the PI Asset Framework database."""

    version = "0.3.0"

    @classmethod
    def servers(cls) -> dict[str, dotnet.AF.PISystem]:
        """Return a dictionary of the known servers."""
        return {server.Name: server for server in dotnet.lib.AF.PISystems()}

    @classmethod
    def default_server(cls) -> dotnet.AF.PISystem | None:
        """Return the default server."""
        if dotnet.lib.AF.PISystems().DefaultPISystem:
            return dotnet.lib.AF.PISystems().DefaultPISystem
        servers = dotnet.lib.AF.PISystems()
        if servers.Count > 0:
            return next(iter(servers))
        else:
            return None

    def __init__(self, server: str | None = None, database: str | None = None) -> None:
        self.server = self._initialise_server(server)
        self.database = self._initialise_database(database)
        self.search = Search.Search(self.database)

    def _initialise_server(self, server: str | None) -> dotnet.AF.PISystem:
        """Initialise the server connection."""
        _logger.debug(f"Initialising server connection from {server!r}")
        default_server = self.default_server()
        if server is None:
            if default_server is None:
                raise ValueError("No server specified and no default server found.")
            _logger.debug(f"Using default server: {default_server.Name}")
            return default_server

        if (_server := dotnet.lib.AF.PISystems()[server]) is not None:
            _logger.debug(_server)
            return _server
        else:
            if default_server is None:
                raise ValueError(
                    f'Server "{server}" not found and no default server found.'
                ) from None
            message = f'Server "{server}" not found, using the default server.'
            _logger.debug(message)
            warnings.warn(message=message, category=UserWarning, stacklevel=2)
            return default_server

    def _initialise_database(self, database: str | None) -> dotnet.AF.AFDatabase:
        def default_db():
            default = self.server.Databases.DefaultDatabase
            if default is None:
                raise ValueError("No database specified and no default database found.")
            return default

        if database is None:
            return default_db()

        if (_db := self.server.Databases[database]) is not None:
            _logger.debug(_db)
            return _db
        else:
            message = f'Database "{database}" not found, using the default database.'
            warnings.warn(message=message, category=UserWarning, stacklevel=2)
            return default_db()

    def __enter__(self) -> Self:
        """Open the PI AF server connection context."""
        self.server.Connect()
        return self

    def __exit__(
        self,
        *args: Any,  # type: ignore
    ) -> bool:
        """Close the PI AF server connection context."""
        _logger.log(0, f"Closing connection to {self} ({args=})")
        return False
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
    def children(self) -> dict[str, Asset.AFElement]:
        """Return a dictionary of the direct child elements of the database."""
        return {c.Name: Asset.AFElement(c) for c in self.database.Elements}

    @property
    def tables(self) -> dict[str, Asset.AFTable]:
        """Return a dictionary of the tables in the database."""
        return {t.Name: Asset.AFTable(t) for t in self.database.Tables}

    def descendant(self, path: str) -> Asset.AFElement:
        """Return a descendant of the database from an exact path."""
        return Asset.AFElement(self.database.Elements.get_Item(path))

    def event_frames(
        self,
        start_time: Time.TimeLike = "",
        start_index: int = 0,
        max_count: int = 1000,
        search_mode: EventFrame.EventFrameSearchMode = _DEFAULT_EVENTFRAME_SEARCH_MODE,
        search_full_hierarchy: bool = False,
    ) -> dict[str, EventFrame.AFEventFrame]:
        """Search for event frames in the database."""
        _start_time = Time.to_af_time(start_time)
        _search_mode = dotnet.lib.AF.EventFrame.AFEventFrameSearchMode(int(search_mode))
        return {
            frame.Name: EventFrame.AFEventFrame(frame)
            for frame in dotnet.lib.AF.EventFrame.AFEventFrame.FindEventFrames(
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


class PIAFDatabase(AFDatabase):
    """Context manager for connections to the PI Asset Framework database."""

    version = "0.3.0"

    def __init__(self, server: str | None = None, database: str | None = None) -> None:
        warnings.warn(
            "PIAFDatabase is deprecated, use AFDatabase instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(server=server, database=database)
