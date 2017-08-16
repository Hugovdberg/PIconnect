"""Storage containers for PI data."""
import datetime

from pandas import Series
import pytz
import wrapt


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


def add_const_to_pi(increment):
    """Return decorator to add data to PI Data for constructing virtual PI Points."""
    @wrapt.decorator
    def adder(func, instance, args, kwargs):
        """Return function value incremented by a fixed value."""
        return func(*args, **kwargs) + increment
    return adder


def add_func_to_pi(increment):
    """Return decorator to add data to PI Data for constructing virtual PI Points."""
    @wrapt.decorator
    def adder(func, instance, args, kwargs):
        """Return function value incremented by a fixed value."""
        return func(*args, **kwargs) + increment(*args, **kwargs)
    return adder
