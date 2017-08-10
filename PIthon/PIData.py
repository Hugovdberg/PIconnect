''' PIData
    Storage containers for PI data
'''

import datetime
from pandas import Series
import pytz


class PISeries(Series):
    'An extension to pandas.Series which always uses the timestamps as index and PI tag as name'

    version = '0.1.0'

    def __init__(self, tag, timestamp, value, uom = None, *args, **kwargs):
        Series.__init__(self,
                        data = value,
                        index = timestamp,
                        name = tag,
                        *args, **kwargs)
        self.tag = tag
        self.uom = uom

    @staticmethod
    def timestamp_to_index(timestamp):
        local_tz = pytz.timezone('Europe/Amsterdam')
        return datetime.datetime(
            timestamp.Year,
            timestamp.Month,
            timestamp.Day,
            timestamp.Hour,
            timestamp.Minute,
            timestamp.Second,
            timestamp.Millisecond*1000
            ).replace(tzinfo = pytz.utc).astimezone(local_tz)


def list_of_strings_recursor(str_f):
    ''' Decorator to make a function that operates on a string (and possibly other
        arguments) also accept a list of strings, and return a single list of results
    '''
    def recursor(string, *args):
        if isinstance(string, list):
            return [y for x in string for y in recursor(x, *args)]
        elif not isinstance(string, basestring):
            raise TypeError('Argument query must be either a string or a list of strings')
        return str_f(string, *args)
    return recursor
