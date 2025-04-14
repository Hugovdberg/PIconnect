"""Time related functions and classes."""

import datetime
import zoneinfo

import pandas as pd  # type: ignore

from PIconnect import dotnet
from PIconnect.config import PIConfig

TimeLike = str | datetime.datetime
IntervalLike = str | datetime.timedelta | pd.Timedelta


def to_af_time_range(start_time: TimeLike, end_time: TimeLike) -> dotnet.AF.Time.AFTimeRange:
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
        :afsdk:`AF.Time.AFTimeRange <T_OSIsoft_AF_Time_AFTimeRange.htm>`:
            Time range covered by the start and end time.
    """
    if isinstance(start_time, datetime.datetime):
        start_time = start_time.isoformat()
    if isinstance(end_time, datetime.datetime):
        end_time = end_time.isoformat()

    return dotnet.lib.AF.Time.AFTimeRange.Parse(start_time, end_time)


def to_af_time(time: TimeLike) -> dotnet.AF.Time.AFTime:
    """Convert a time to a AFTime value.

    Parameters
    ----------
        time (str | datetime): Time to convert to AFTime.

    Returns
    -------
        :afsdk:`AF.Time.AFTime <T_OSIsoft_AF_Time_AFTime.htm>`:
            AFTime version of time.
    """
    if isinstance(time, datetime.datetime):
        time = time.isoformat()

    return dotnet.lib.AF.Time.AFTime(time)


def to_af_time_span(interval: IntervalLike | None) -> dotnet.AF.Time.AFTimeSpan:
    """Convert a time interval to a AFTimeSpan value.

    Parameters
    ----------
        interval (str | datetime.timedelta | pd.Timedelta): Interval to convert to AFTimeSpan.

    Returns
    -------
        :afsdk:`AF.Time.AFTimeSpan <T_OSIsoft_AF_Time_AFTimeSpan.htm>`:
            AFTimeSpan version of interval.
    """
    if isinstance(interval, (datetime.timedelta, pd.Timedelta)):
        interval = f"{interval.total_seconds()}s"

    return dotnet.lib.AF.Time.AFTimeSpan.Parse(interval)


def timestamp_to_index(timestamp: dotnet.System.DateTime) -> datetime.datetime:
    """Convert AFTime object to datetime in local timezone.

    Parameters
    ----------
        timestamp (`System.DateTime`): Timestamp in .NET format to convert to `datetime`.

    Returns
    -------
        `datetime`: Datetime with the timezone info from :data:`PIConfig.DEFAULT_TIMEZONE <PIconnect.config.PIConfigContainer.DEFAULT_TIMEZONE>`.
    """  # noqa: E501
    local_tz = zoneinfo.ZoneInfo(PIConfig.DEFAULT_TIMEZONE)
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
        .replace(tzinfo=datetime.timezone.utc)
        .astimezone(local_tz)
    )
