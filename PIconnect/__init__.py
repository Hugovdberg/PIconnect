"""PIconnect - Connector to the OSISoft PI and PI-AF databases."""

from PIconnect.AFSDK import AF, AF_SDK_VERSION
from PIconnect.config import PIConfig
from PIconnect.PI import PIServer
from PIconnect.PIAF import PIAFDatabase

from . import _version

__version__ = _version.get_versions()["version"]
__sdk_version = tuple(int(x) for x in AF.PISystems().Version.split("."))

__all__ = [
    "AF",
    "AF_SDK_VERSION",
    "PIAFDatabase",
    "PIConfig",
    "PIServer",
    "__sdk_version",
]
