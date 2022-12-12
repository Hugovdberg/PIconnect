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

pythonnet.load()


def __fallback():
    import enum
    import warnings

    warnings.warn("Can't import the PI AF SDK, running in test mode", ImportWarning)
    AF_SDK_VERSION = "2.7_compatible"
    # pragma pylint: disable=invalid-name, unused-argument, too-few-public-methods
    class AF:
        """Mock class of the AF namespace"""

        class Data:
            """Mock class of the AF.Data namespace"""

            class AFBoundaryType(enum.IntEnum):
                """Mock class of the AF.Data.AFBoundaryType enumeration"""

                Inside = 0
                Outside = 1
                Interpolated = 2

        class PI:
            """Mock class of the AF.PI namespace"""

            class PIPoint:
                """Mock class of the AF.PI.PIPoint class"""

                Name: str
                """This property identifies the name of the PIPoint"""

                @staticmethod
                def FindPIPoints(connection, query, source, attribute_names):
                    """Stub to mock querying PIPoints"""
                    return []

            class PIServer:
                """Mock class of the AF.PI.PIServer class"""

                def __init__(self, name):
                    self.Name = name

                def Connect(self, retry):
                    """Stub for connecting to test server"""
                    pass

                def Disconnect(self):
                    """Stub for disconnecting from test server"""
                    pass

            class PIServers:
                """Mock class of the AF.PI.PIServers class"""

                DefaultPIServer = None

                def __init__(self):
                    self._init()

                def _init(self):
                    if not self.DefaultPIServer:
                        self.DefaultPIServer = AF.PI.PIServer("Testing")

                def __iter__(self):
                    self._init()
                    return (x for x in [self.DefaultPIServer])

        class AFElement:
            """Mock class of the AF.AFElement class"""

            def __init__(self, name):
                self.Name = name

        class AFDatabase:
            """Mock class of the AF.AFDatabase class"""

            def __init__(self, name):
                self.Name = name
                self.Elements = [AF.AFElement("TestElement")]

        class PISystem:
            """Mock class of the AF.PISystem class"""

            class InternalDatabases:
                """Mock class for the AF.PISystem.Databases property"""

                def __init__(self):
                    self.DefaultDatabase = AF.AFDatabase("TestDatabase")

                def __iter__(self):
                    return (x for x in [self.DefaultDatabase])

            def __init__(self, name):
                self.Name = name
                self.Databases = AF.PISystem.InternalDatabases()

            def Connect(self):
                """Stub to connect to the testing system"""
                pass

            def Disconnect(self):
                """Stub to disconnect from the testing system"""

                pass

        class PISystems:
            """Mock class of the AF.PISystems class"""

            DefaultPISystem = None
            Version = "0.0.0.0"

            def __init__(self):
                self._init()

            def _init(self):
                if not self.DefaultPISystem:
                    self.DefaultPISystem = AF.PISystem("TestingAF")

            def __iter__(self):
                self._init()
                return (x for x in [self.DefaultPISystem])

        class Time:
            """Mock class of the AF.Time namespace"""

            class AFTimeRange:
                """Mock class of the AF.Time.AFTimeRange class"""

                def __init__(self, start_time, end_time):
                    pass

            class AFTimeSpan:
                """Mock class of the AF.Time.AFTimeSpan class"""

                def __init__(self):
                    pass

                @staticmethod
                def Parse(interval):
                    """Stub for parsing strings that should return a AFTimeSpan"""
                    return AF.Time.AFTimeSpan()

    # pragma pylint: enable=invalid-name, unused-argument, too-few-public-methods
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
