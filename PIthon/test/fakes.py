"""Fake classes to mask SDK complexity"""


class FakeAFTime(object):
    """Fake AFTime to mask away SDK complexity."""
    def __init__(self, timestamp):
        self.UtcTime = lambda x: None
        self.UtcTime.Year = timestamp.year
        self.UtcTime.Month = timestamp.month
        self.UtcTime.Day = timestamp.day
        self.UtcTime.Hour = timestamp.hour
        self.UtcTime.Minute = timestamp.minute
        self.UtcTime.Second = timestamp.second
        self.UtcTime.Millisecond = int(timestamp.microsecond / 1000)


class FakeAFValue(object):
    """Fake AFValue to mask away SDK complexity."""
    def __init__(self, value, timestamp):
        self.Value = value
        self.Timestamp = FakeAFTime(timestamp)


class FakePIPoint(object):
    """Fake PI Point to mask away SDK complexity."""
    def __init__(self, values, timestamps):
        self.call_stack = ['FakePIPoint created']
        self.values = [FakeAFValue(value, timestamp)
                       for value, timestamp in zip(values, timestamps)]

    def CurrentValue(self):
        self.call_stack.append('CurrentValue called')
        return self.values[-1]
