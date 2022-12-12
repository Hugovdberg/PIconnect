class DateTime:
    """Mock for System.DateTime"""

    def __init__(self) -> None:
        pass


class AFTime:
    """Mock class of the AF.Time.AFTime class"""

    def __init__(self, time: str) -> None:
        self.UtcTime: DateTime


class AFTimeRange:
    """Mock class of the AF.Time.AFTimeRange class"""

    def __init__(self, start_time, end_time):
        pass


class AFTimeSpan:
    """Mock class of the AF.Time.AFTimeSpan class"""

    def __init__(self):
        pass

    @staticmethod
    def Parse(interval: str, /) -> "AFTimeSpan":
        """Stub for parsing strings that should return a AFTimeSpan"""
        return AFTimeSpan()
