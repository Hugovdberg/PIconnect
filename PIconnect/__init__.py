""" PIconnect
    Connector to the OSISoft PI and PI-AF databases.
"""
# pragma pylint: disable=unused-import
from PIconnect.AFSDK import AF, AF_SDK_VERSION
from PIconnect.config import PIConfig
from PIconnect.PI import PIServer
from PIconnect.PIAF import PIAFDatabase

# pragma pylint: enable=unused-import

__version__ = "0.10.6"
__sdk_version = tuple(int(x) for x in AF.PISystems().Version.split("."))

__all__ = [
    "AF",
    "AF_SDK_VERSION",
    "PIAFDatabase",
    "PIConfig",
    "PIServer",
    "__sdk_version",
]
