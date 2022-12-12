from typing import Any, Dict, List
import Asset
import Time


class PIPoint:
    """Mock class of the AF.PI.PIPoint class"""

    Name: str = "TestPIPoint"
    """This property identifies the name of the PIPoint"""

    @staticmethod
    def FindPIPoints(connection, query, source, attribute_names):
        """Stub to mock querying PIPoints"""
        return []

    @staticmethod
    def GetAttributes(names: List[str]) -> Dict[str, Any]:  # type: ignore
        pass

    @staticmethod
    def LoadAttributes(params: List[str], /) -> None:
        pass

    @staticmethod
    def InterpolatedValue(time: Time.AFTime) -> Asset.AFValue:  # type: ignore
        pass

    @staticmethod
    def CurrentValue() -> Asset.AFValue:  # type: ignore
        pass


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
            self.DefaultPIServer = PIServer("Testing")

    def __iter__(self):
        self._init()
        return (x for x in [self.DefaultPIServer])
