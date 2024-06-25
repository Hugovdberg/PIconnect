"""PIconnect - Connector to the OSISoft PI and PI-AF databases."""

from PIconnect.AFSDK import AF, AF_SDK_VERSION, get_PI_connector
from PIconnect.config import PIConfig
from PIconnect.PI import PIServer
from PIconnect.PIAF import PIAFDatabase

__version__ = "0.12.0"
__sdk_version = tuple(int(x) for x in AF.PISystems().Version.split("."))

__all__ = [
    "AF",
    "AF_SDK_VERSION",
    "PIAFDatabase",
    "PIConfig",
    "PIServer",
    "get_PI_connector",
    "__sdk_version",
]
