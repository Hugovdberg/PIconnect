"""Time related functions and classes."""

# pyright: strict
import datetime
from typing import Union

import pytz

from PIconnect import AF, PIConfig
from PIconnect.AFSDK import System

TimeLike = Union[str, datetime.datetime]


def to_af_time_range(start_time: TimeLike, end_time: TimeLike) -> AF.Time.AFTimeRange:
    """Convert a combination of start and end time to a time range.

    Both `start_time` and `end_time` can be either a :any:`datetime.datetime` object or
    a string.
    `datetime` objects are first converted to a string, before being passed to
    :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
    It is also possible to specify either end as a `datetime` object,
    and then specify the other boundary as a relative string.

    Parameters
    ----------
        start_time (str | datetime): Start time of the time range.
        end_time (str | datetime): End time of the time range.

    Returns
    -------
        :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`:
            Time range covered by the start and end time.
    """
    if isinstance(start_time, datetime.datetime):
        start_time = start_time.isoformat()
    if isinstance(end_time, datetime.datetime):
        end_time = end_time.isoformat()

    return AF.Time.AFTimeRange.Parse(start_time, end_time)


def to_af_time(time: TimeLike) -> AF.Time.AFTime:
    """Convert a time to a AFTime value.

    Parameters
    ----------
        time (str | datetime): Time to convert to AFTime.

    Returns
    -------
        :afsdk:`AF.Time.AFTime <M_OSIsoft_AF_Time_AFTime__ctor_7.htm>`:
            AFTime version of time.
    """
    if isinstance(time, datetime.datetime):
        time = time.isoformat()

    return AF.Time.AFTime(time)


def timestamp_to_index(timestamp: System.DateTime) -> datetime.datetime:
    """Convert AFTime object to datetime in local timezone.

    Parameters
    ----------
        timestamp (`System.DateTime`): Timestamp in .NET format to convert to `datetime`.

    Returns
    -------
        `datetime`: Datetime with the timezone info from :data:`PIConfig.DEFAULT_TIMEZONE <PIconnect.config.PIConfigContainer.DEFAULT_TIMEZONE>`.
    """  # noqa: E501
    local_tz = pytz.timezone(PIConfig.DEFAULT_TIMEZONE)
    return (
        datetime.datetime(
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
