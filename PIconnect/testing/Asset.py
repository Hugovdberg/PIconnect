import Time


class AFValue:
    def __init__(self):
        self.Timestamp: Time.AFTime


class AFBaseElement:
    pass


class AFElement(AFBaseElement):
    """Mock class of the AF.AFElement class"""

    def __init__(self, name):
        self.Name = name
