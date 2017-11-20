""" PIData
    Storage containers for PI data.
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

import datetime
from pandas import Series
import pytz


class PISeries(Series):
    """Extension to pandas.Series with PI metadata."""
    version = '0.1.0'

    def __init__(self, tag, timestamp, value, uom=None, *args, **kwargs):
        Series.__init__(self,
                        data=value,
                        index=timestamp,
                        name=tag,
                        *args, **kwargs)
        self.tag = tag
        self.uom = uom

    @staticmethod
    def timestamp_to_index(timestamp):
        """Convert AFTime object to datetime.datetime in local timezone.

           TODO: Allow to define timezone, default to UTC?
        """
        local_tz = pytz.timezone('Europe/Amsterdam')
        return datetime.datetime(
            timestamp.Year,
            timestamp.Month,
            timestamp.Day,
            timestamp.Hour,
            timestamp.Minute,
            timestamp.Second,
            timestamp.Millisecond * 1000
        ).replace(tzinfo=pytz.utc).astimezone(local_tz)
