""" AFSDK
    Loads the .NET libraries from the OSIsoft AF SDK
"""
import os
import sys
import typing
import logging

import pythonnet

__all__ = ["AF", "AF_SDK_VERSION"]

logger = logging.getLogger(__name__)

pythonnet.load("netfx")


def __fallback():
    import warnings

    warnings.warn("Can't import the PI AF SDK, running in test mode", ImportWarning)

    from .testing import AF, AF_SDK_VERSION

    return AF, AF_SDK_VERSION


if os.getenv("GITHUB_ACTIONS") == "true":
    AF, AF_SDK_VERSION = __fallback()
else:
    import clr

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

    from OSIsoft import AF  # type: ignore ; pylint: wrong-import-position

    AF_SDK_VERSION = AF.PISystems().Version
    print("OSIsoft(r) AF SDK Version: {}".format(AF_SDK_VERSION))


if typing.TYPE_CHECKING:
    # This branch is separate from previous one as otherwise no typechecking takes place
    # on the main logic.
    AF, AF_SDK_VERSION = __fallback()
