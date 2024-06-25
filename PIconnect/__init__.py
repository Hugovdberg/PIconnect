"""PIconnect - Connector to the OSISoft PI and PI-AF databases."""

from PIconnect.config import PIConfig  # noqa: I001 isort: skip
from PIconnect.AF import AFDatabase, PIAFDatabase
from PIconnect.AFSDK import AF, AF_SDK_VERSION
from PIconnect.PI import PIServer

from . import _version

__version__ = _version.get_versions()["version"]
__sdk_version = tuple(int(x) for x in AF_SDK_VERSION.split("."))

__all__ = [
    "AF",
    "AF_SDK_VERSION",
    "AFDatabase",
    "PIAFDatabase",
    "PIConfig",
    "PIConnector",
    "PIServer",
    "__sdk_version",
]
