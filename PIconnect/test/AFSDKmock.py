import enum


class AF:
    class Data:
        class AFBoundaryType(enum.IntEnum):
            Inside = 0
            Outside = 1
            Interpolated = 2

    class PI:
        class PIServer:
            def __init__(self, name):
                self.Name = name

        class PIServers:
            def __init__(self):
                self.DefaultPIServer = AF.PI.PIServer('Testing')

            def __iter__(self):
                return (x for x in [self.DefaultPIServer])

    class PISystem:
        def __init__(self, name):
            self.Name = name

    class PISystems:
        def __init__(self):
            self.DefaultPISystem = AF.PISystem('TestingAF')

        def __iter__(self):
            return (x for x in [self.DefaultPISystem])
