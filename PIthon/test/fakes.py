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


class FakeKeyValue(object):
    """Container for fake Key:Value pairs"""
    def __init__(self, key, value):
        self.Key = key
        self.Value = value


class FakeAFValue(object):
    """Fake AFValue to mask away SDK complexity."""
    def __init__(self, value, timestamp):
        self.Value = value
        self.Timestamp = FakeAFTime(timestamp)


class FakePIPoint(object):
    """Fake PI Point to mask away SDK complexity."""
    def __init__(self, tag, values, timestamps, attributes):
        self.Name = tag
        self.call_stack = ['FakePIPoint created']
        self.values = [FakeAFValue(value, timestamp)
                       for value, timestamp in zip(values, timestamps)]
        self.attributes = [FakeKeyValue(*att) for att in attributes.iteritems()]

    def CurrentValue(self):
        self.call_stack.append('CurrentValue called')
        return self.values[-1]

    def LoadAttributes(self, *args, **kwargs):
        self.call_stack.append('LoadAttributes called')

    def GetAttributes(self, *args, **kwargs):
        self.call_stack.append('GetAttributes called')
        return self.attributes

    def RecordedValues(self, *args, **kwargs):
        self.call_stack.append('RecordedValues called')
        return self.values

    def InterpolatedValues(self, *args, **kwargs):
        self.call_stack.append('InterpolatedValues called')
        return self.values
