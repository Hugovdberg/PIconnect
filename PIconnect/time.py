from datetime import datetime
from typing import Union

from PIconnect.AFSDK import AF


def to_af_time_range(start_time: Union[str, datetime], end_time: Union[str, datetime]):
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
