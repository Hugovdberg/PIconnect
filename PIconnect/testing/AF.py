import Asset
import Data
import Time
import PI

__all__ = ["Asset", "Data", "Time", "PI", "AFDatabase"]


class AFDatabase:
    """Mock class of the AF.AFDatabase class"""

    def __init__(self, name):
        self.Name = name
        self.Elements = [Asset.AFElement("TestElement")]


class PISystem:
    """Mock class of the AF.PISystem class"""

    class InternalDatabases:
        """Mock class for the AF.PISystem.Databases property"""

        def __init__(self):
            self.DefaultDatabase = AFDatabase("TestDatabase")

        def __iter__(self):
            return (x for x in [self.DefaultDatabase])

    def __init__(self, name):
        self.Name = name
        self.Databases = PISystem.InternalDatabases()

    def Connect(self):
        """Stub to connect to the testing system"""

    def Disconnect(self):
        """Stub to disconnect from the testing system"""


class PISystems:
    """Mock class of the AF.PISystems class"""

    DefaultPISystem = None
    Version = "0.0.0.0"

    def __init__(self):
        self._init()

    def _init(self):
        if not self.DefaultPISystem:
            self.DefaultPISystem = PISystem("TestingAF")

    def __iter__(self):
        self._init()
        return (x for x in [self.DefaultPISystem])
