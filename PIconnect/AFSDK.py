""" AFSDK
    Loads the .NET libraries from the OSIsoft AF SDK
"""
# Copyright 2017 Hugo van den Berg, Stijn de Jong

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pragma pylint: disable=unused-import
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (
    bytes,
    dict,
    int,
    list,
    object,
    range,
    str,
    ascii,
    chr,
    hex,
    input,
    next,
    oct,
    open,
    pow,
    round,
    super,
    filter,
    map,
    zip,
)

# pragma pylint: enable=unused-import
import sys
import os

try:
    import clr

    # Get the installation directory from the environment variable or fall back
    # to the Windows default installation path
    PIAF_SDK = os.getenv("PIHOME", "C:\\Program Files\\PIPC")
    PIAF_SDK += "\\AF\\PublicAssemblies\\4.0\\"
    if not os.path.isdir(PIAF_SDK):
        raise ImportError("PIAF SDK not found in %s, check installation" % PIAF_SDK)

    sys.path.append(PIAF_SDK)
    clr.AddReference("OSIsoft.AFSDK")  # pylint: disable=no-member

    from OSIsoft import AF  # pylint: wrong-import-position
except ImportError:
    import enum
    import warnings

    warnings.warn("Can't import the PI AF SDK, running in test mode", ImportWarning)

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
