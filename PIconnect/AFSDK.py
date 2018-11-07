''' AFSDK
    Loads the .NET libraries from the OSIsoft AF SDK
'''
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
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str,
                      ascii, chr, hex, input, next, oct, open,
                      pow, round, super,
                      filter, map, zip)
# pragma pylint: enable=unused-import
import sys
import os

try:
    import clr

    # Get the installation directory from the environment variable or fall back
    # to the Windows default installation path
    PIAF_SDK = os.getenv('PIHOME', 'C:\\Program Files\\PIPC')
    PIAF_SDK += '\\AF\\PublicAssemblies\\4.0\\'
    if not os.path.isdir(PIAF_SDK):
        raise ImportError(
            'PIAF SDK not found in %s, check installation' % PIAF_SDK)

    sys.path.append(PIAF_SDK)
    clr.AddReference('OSIsoft.AFSDK')  # pylint: disable=no-member

    from OSIsoft import AF  # pylint: wrong-import-position
except ImportError:
    import enum
    import warnings
    warnings.warn("Can't import the PI AF SDK, running in test mode",
                  ImportWarning)

    class AF:
        class Data:
            class AFBoundaryType(enum.IntEnum):
                Inside = 0
                Outside = 1
                Interpolated = 2

        class PI:
            class PIPoint:
                @staticmethod
                def FindPIPoints(connection, query, source, attribute_names):
                    return []

            class PIServer:
                def __init__(self, name):
                    self.Name = name

                def Connect(self, retry):
                    pass

                def Disconnect(self):
                    pass

            class PIServers:
                DefaultPIServer = None

                def __init__(self):
                    self._init()

                def _init(self):
                    if not self.DefaultPIServer:
                        self.DefaultPIServer = AF.PI.PIServer('Testing')

                def __iter__(self):
                    self._init()
                    return (x for x in [self.DefaultPIServer])

        class AFElement:
            def __init__(self, name):
                self.Name = name

        class AFDatabase:
            def __init__(self, name):
                self.Name = name
                self.Elements = [AF.AFElement('TestElement')]

        class PISystem:
            class _Databases:
                DefaultDatabase = None

                def __init__(self):
                    self._init()

                @classmethod
                def _init(cls):
                    if not cls.DefaultDatabase:
                        cls.DefaultDatabase = AF.AFDatabase('TestDatabase')

                def __iter__(self):
                    self._init()
                    return (x for x in [self.DefaultDatabase])

            def __init__(self, name):
                self.Name = name
                self.Databases = AF.PISystem._Databases()

            def Connect(self):
                pass

            def Disconnect(self):
                pass

        class PISystems:
            DefaultPISystem = None

            def __init__(self):
                self._init()

            def _init(self):
                if not self.DefaultPISystem:
                    self.DefaultPISystem = AF.PISystem('TestingAF')

            def __iter__(self):
                self._init()
                return (x for x in [self.DefaultPISystem])

        class Time:
            class AFTimeRange:
                def __init__(self, start_time, end_time):
                    pass

            class AFTimeSpan:
                def __init__(self):
                    pass

                @staticmethod
                def Parse(interval):
                    return AF.Time.AFTimeSpan()
    # AF.PISystems().DefaultPISystem.Databases()._init()
