""" PIconnect.test.fakes
    Fake classes to mask SDK complexity
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
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, dict, int, list, object, range, str,
                      ascii, chr, hex, input, next, oct, open,
                      pow, round, super,
                      filter, map, zip)
# pragma pylint: enable=unused-import
import datetime
import unittest2

import pytz

import PIconnect as PI
from PIconnect._operators import add_operators, OPERATORS


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


class FakePIPoint_(object):
    def __init__(self, tag, values, timestamps, attributes):
        self.Name = tag
        self.values = [FakeAFValue(value, timestamp)
                       for value, timestamp in zip(values, timestamps)]
        self.attributes = [FakeKeyValue(*att) for att in attributes.items()]


@add_operators(
    operators=OPERATORS,
    members=[
        '_current_value',
        'sampled_data'
    ],
    newclassname='VirtualFakePIPoint',
    attributes=['pi_point']
)
class FakePIPoint(object):
    """Fake PI Point to mask away SDK complexity."""

    def __init__(self, pi_point):
        self.pi_point = pi_point
        self.call_stack = ['%s created' % self.__class__.__name__]
        self.Name = pi_point.Name

    def CurrentValue(self):
        self.call_stack.append('CurrentValue called')
        return self.pi_point.values[-1]

    def LoadAttributes(self, *args, **kwargs):
        self.call_stack.append('LoadAttributes called')

    def GetAttributes(self, *args, **kwargs):
        self.call_stack.append('GetAttributes called')
        return self.pi_point.attributes

    def RecordedValues(self, *args, **kwargs):
        self.call_stack.append('RecordedValues called')
        return self.pi_point.values

    def InterpolatedValues(self, *args, **kwargs):
        self.call_stack.append('InterpolatedValues called')
        return self.pi_point.values


class VirtualTestCase(unittest2.TestCase):
    """Test VirtualPIPoint addition."""

    def setUp(self):
        self.tag = 'TEST_140_053_FQIS053_01_Meetwaarde'
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.timestamp_numbers = [
            1502654535.813,
            1502671554.038,
            1502695584.315,
            1502704569.874,
            1502709576.898,
            1502713512.168,
            1502718534.453,
            1502722585.816,
            1502731598.316,
            1502732545.013
        ]
        self.timestamps = [datetime.datetime.fromtimestamp(x, tz=pytz.utc)
                           for x in self.timestamp_numbers]
        self.attributes = {
            'engunits': 'm3/h',
            'descriptor': 'Flow'
        }
        pi_point = FakePIPoint_(tag=self.tag,
                                values=self.values,
                                timestamps=self.timestamps,
                                attributes=self.attributes)
        self.point = PI.PI.PIPoint(FakePIPoint(pi_point))
