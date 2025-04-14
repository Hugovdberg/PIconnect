"""PIconnect - Connector to the OSISoft PI and PI-AF databases."""

from PIconnect.config import PIConfig  # noqa: I001 isort: skip
from PIconnect.AF import AFDatabase, PIAFDatabase
from PIconnect.dotnet import lib, load_SDK
from PIconnect.PI import PIServer

from . import _version


def __getattr__(name: str):
    """Lazy load the AF SDK."""
    match name:
        case "__sdk_version":
            return tuple(int(x) for x in lib.AF_SDK_VERSION.split("_")[0].split("."))
        case _:
            raise AttributeError(f"module {__name__} has no attribute {name}")


__version__ = _version.get_versions()["version"]

__all__ = [
    "AFDatabase",
    "PIAFDatabase",
    "PIConfig",
    "PIServer",
    "load_SDK",
]
