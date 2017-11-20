""" PIthon.test.fakes
    Fake classes to mask SDK complexity
"""
# Copyright 2017 Hugo van den Berg, Stijn de Jong

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
