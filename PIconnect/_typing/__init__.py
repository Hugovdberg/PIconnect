"""Type stubs for the AF SDK and dotnet libraries."""

from . import dotnet as System  # noqa: I001
from . import AF

AF_SDK_VERSION = "2.7_compatible"

__all__ = ["AF", "AF_SDK_VERSION", "System"]
