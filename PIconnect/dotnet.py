"""AFSDK - Loads the .NET libraries from the OSIsoft AF SDK."""

import logging
import os
import pathlib
import sys
from typing import cast

from ._typing import AF, AF_SDK_VERSION, AFType, System, SystemType

__all__ = ["AF", "System", "AF_SDK_VERSION", "lib", "load_SDK"]

logger = logging.getLogger(__name__)

StrPath = str | pathlib.Path


class dotNET:
    """Class to load the .NET libraries from the OSIsoft AF SDK."""

    def __init__(self) -> None:
        self._af: AFType | None = None
        self._system: SystemType | None = None
        self._af_sdk_version: str | None = None

    @property
    def AF(self) -> AFType:
        """Return the AF SDK."""
        if self._af is None:
            raise ImportError(".NET libraries not loaded, call PIconnect.load_SDK() first.")
        return self._af

    @property
    def System(self) -> SystemType:
        """Return the System SDK."""
        if self._system is None:
            raise ImportError(".NET libraries not loaded, call PIconnect.load_SDK() first.")
        return self._system

    @property
    def AF_SDK_VERSION(self) -> str:
        """Return the AF SDK version."""
        return self.AF.PISystems().Version

    def load(self, assembly_path: StrPath | None = None) -> None:
        """Return a new instance of the PI connector."""
        full_path = _get_SDK_path(assembly_path)
        if full_path is None:
            if assembly_path:
                raise ImportError(f"AF SDK not found at '{assembly_path}'")
            raise ImportError(
                "AF SDK not found, check installation "
                "or pass valid path to directory containing SDK assembly."
            )
        self._af, self._system = _get_dotnet_libraries(full_path)
        self._af_sdk_version = self.AF.PISystems().Version
        logger.info("Loaded AF SDK version %s", self._af_sdk_version)

    def load_test_SDK(self) -> None:
        self._af = AF
        self._system = System
        self._af_sdk_version = AF_SDK_VERSION


def _get_dotnet_libraries(full_path: StrPath) -> tuple[AFType, SystemType]:
    import clr  # type: ignore

    sys.path.append(str(full_path))
    clr.AddReference("OSIsoft.AFSDK")  # type: ignore ; pylint: disable=no-member
    import System  # type: ignore
    from OSIsoft import AF  # type: ignore

    _AF = cast(AFType, AF)
    _System = cast(SystemType, System)
    return _AF, _System


def _get_SDK_path(full_path: StrPath | None = None) -> pathlib.Path | None:
    if full_path:
        assembly_directories = [pathlib.Path(full_path)]
    else:
        installation_directories = {
            os.getenv("PIHOME"),
            "C:\\Program Files\\PIPC",
            "C:\\Program Files (x86)\\PIPC",
        }
        assembly_directories = (
            pathlib.Path(path) / "AF\\PublicAssemblies\\4.0\\"
            for path in installation_directories
            if path is not None
        )
    for AF_dir in assembly_directories:
        logging.debug("Full path to potential SDK location: '%s'", AF_dir)
        if AF_dir.is_dir():
            return AF_dir


lib = dotNET()


def load_SDK(assembly_path: StrPath | None = None) -> None:
    """Load the AF SDK from the specified path.

    Parameters
    ----------
        assembly_path (str | Path, optional): Path to the AF SDK assembly. If None, the default
            installation path will be used.

    Raises
    ------
        ImportError: If the AF SDK cannot be found or loaded.
    """
    global lib
    lib.load(assembly_path)
