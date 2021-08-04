from datetime import datetime
import pytz

from PIconnect.AFSDK import AF
from PIconnect.config import PIConfig


def to_af_time_range(start_time, end_time):
    """to_af_time_range

    Return AF.Time.AFTimeRange object from datetime or string
    using :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.

    If string is used, it is assumed that user knows the format
    that should be passed to AF.Time.AFTimeRange.
    """

    if isinstance(start_time, datetime):
        start_time = start_time.isoformat()
    if isinstance(end_time, datetime):
        end_time = end_time.isoformat()

    return AF.Time.AFTimeRange(start_time, end_time)


def timestamp_to_index(timestamp):
    """Convert AFTime object to datetime in local timezone.

    .. todo::

        Allow to define timezone, default to UTC?

    .. todo::

    """
    local_tz = pytz.timezone(PIConfig.DEFAULT_TIMEZONE)
    return (
        datetime(
            timestamp.Year,
            timestamp.Month,
            timestamp.Day,
            timestamp.Hour,
            timestamp.Minute,
            timestamp.Second,
            timestamp.Millisecond * 1000,
        )
        .replace(tzinfo=pytz.utc)
        .astimezone(local_tz)
    )
