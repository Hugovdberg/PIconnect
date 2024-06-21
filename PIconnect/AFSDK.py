"""AFSDK - Loads the .NET libraries from the OSIsoft AF SDK."""

import logging
import os
import sys
import typing

__all__ = ["AF", "System", "AF_SDK_VERSION"]

logger = logging.getLogger(__name__)

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
    from ._typing import dotnet as _System

    return _af, _System, _AF_SDK_version


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
    installation_directories = [
        os.getenv("PIHOME"),
        "C:\\Program Files\\PIPC",
        "C:\\Program Files (x86)\\PIPC",
    ]
    for directory in installation_directories:
        logging.debug("Trying installation directory '%s'", directory)
        if not directory:
            continue
        AF_dir = os.path.join(directory, "AF\\PublicAssemblies\\4.0\\")
        logging.debug("Full path to potential SDK location: '%s'", AF_dir)
        if os.path.isdir(AF_dir):
            PIAF_SDK = AF_dir
            break
    else:
        raise ImportError("PIAF SDK not found, check installation")

    sys.path.append(PIAF_SDK)

    clr.AddReference("OSIsoft.AFSDK")  # type: ignore ; pylint: disable=no-member

    import System as _System  # type: ignore
    from OSIsoft import AF as _af  # type: ignore

    _AF_SDK_version = typing.cast(str, _af.PISystems().Version)  # type: ignore ; pylint: disable=no-member
    print("OSIsoft(r) AF SDK Version: {}".format(_AF_SDK_version))


if typing.TYPE_CHECKING:
    # This branch is separate from previous one as otherwise no typechecking takes place
    # on the main logic.
    _af, _System, _AF_SDK_version = __fallback()

AF = _af
System = _System
AF_SDK_VERSION = _AF_SDK_version
