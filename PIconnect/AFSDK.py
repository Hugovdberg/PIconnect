"""AFSDK - Loads the .NET libraries from the OSIsoft AF SDK."""

import dataclasses
import logging
import os
import pathlib
import sys
from types import ModuleType
from typing import TYPE_CHECKING, Optional, Union, cast

__all__ = ["AF", "System", "AF_SDK_VERSION"]

logger = logging.getLogger(__name__)


@dataclasses.dataclass(kw_only=True)
class PIConnector:
    assembly_path: pathlib.Path
    AF: ModuleType
    System: ModuleType


StrPath = Union[str, pathlib.Path]


def get_PI_connector(assembly_path: Optional[StrPath] = None) -> PIConnector:
    """Return a new instance of the PI connector."""
    full_path = _get_SDK_path(assembly_path)
    if full_path is None:
        if assembly_path:
            raise ImportError(f"PIAF SDK not found at '{assembly_path}'")
        raise ImportError(
            "PIAF SDK not found, check installation "
            "or pass valid path to directory containing SDK assembly."
        )
    dotnetSDK = _get_dotnet_SDK(full_path)
    return PIConnector(assembly_path=full_path, **dotnetSDK)


def _get_dotnet_SDK(full_path: pathlib.Path) -> dict[str, ModuleType]:
    import clr  # type: ignore

    sys.path.append(str(full_path))
    clr.AddReference("OSIsoft.AFSDK")  # type: ignore ; pylint: disable=no-member
    import System  # type: ignore
    from OSIsoft import AF  # type: ignore

    _AF = cast(ModuleType, AF)
    _System = cast(ModuleType, System)
    return {"AF": _AF, "System": _System}


# pragma pylint: disable=import-outside-toplevel


def __fallback():
    import warnings

    warnings.warn(
        "Can't import the PI AF SDK, running in test mode",
        ImportWarning,
        stacklevel=2,
    )

    from ._typing import AF as _af
    from ._typing import AF_SDK_VERSION as _AF_SDK_version
    from ._typing import System as _System

    return _af, _System, _AF_SDK_version


def _get_SDK_path(full_path: Optional[StrPath] = None) -> Optional[pathlib.Path]:
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


if (
    os.getenv("GITHUB_ACTIONS", "false").lower() == "true"
    or os.getenv("TF_BUILD", "false").lower() == "true"
    or os.getenv("READTHEDOCS", "false").lower() == "true"
):
    _af, _System, _AF_SDK_version = __fallback()
else:
    import clr  # type: ignore

    # Get the installation directory from the environment variable or fall back
    # to the Windows default installation path
    PIAF_SDK = _get_SDK_path()
    if PIAF_SDK is None:
        raise ImportError("PIAF SDK not found, check installation")

    sys.path.append(str(PIAF_SDK))

    clr.AddReference("OSIsoft.AFSDK")  # type: ignore ; pylint: disable=no-member

    import System as _System  # type: ignore
    from OSIsoft import AF as _af  # type: ignore

    _AF_SDK_version = cast(str, _af.PISystems().Version)  # type: ignore ; pylint: disable=no-member
    print("OSIsoft(r) AF SDK Version: {}".format(_AF_SDK_version))


if TYPE_CHECKING:
    # This branch is separate from previous one as otherwise no typechecking takes place
    # on the main logic.
    _af, _System, _AF_SDK_version = __fallback()

AF = _af
System = _System
AF_SDK_VERSION = _AF_SDK_version
