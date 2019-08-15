====================
Extracting summaries
====================

Extracting a summary for a single time interval
-----------------------------------------------

The PI system allows multiple types of summaries to be calculated from data.
To get the maximum value of a :any:`PIPoint` in the last 14 days, you would
use the :any:`PIPoint.summary` method as shown in the following code::

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary('*-14d', '*', SummaryType.MAXIMUM)
        print(data)

The returned `data` is a :class:`pandas.DataFrame` with the time stamps as
index and a column for each requested summary. The time stamp in this case
is the datetime at which the maximum occurred. This is more obvious when
requesting multiple summaries over the same time span::

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary('*-14d', '*', SummaryType.MAXIMUM|SummaryType.MINIMUM)
        print(data)

Since the minimum and maximum of a point never occur at the same time stamp,
the :class:`DataFrame` in the previous example will typically occur two row.
It is possible to reduce that to a single time stamp, when the time at which
the summary value occurs is of no value.

There are two possibilities for the time stamp, the beginning of the requested
time interval, or the end of the interval. Which to return is specified using
the `time_type` argument. To always return the beginning of the interval, you
should use the :any:`TimestampCalculation.EARLIEST_TIME` constant from
:any:`PIConsts`::

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType, TimestampCalculation

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary(
            '*-14d',
            '*',
            SummaryType.MAXIMUM|SummaryType.MINIMUM,
            time_type=TimestampCalculation.EARLIEST_TIME
        )
        print(data)

Similarly, the :any:`TimestampCalculation.MOST_RECENT_TIME` constant always
returns the time at the end of the interval::

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType, TimestampCalculation

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary(
            '*-14d',
            '*',
            SummaryType.MAXIMUM|SummaryType.MINIMUM,
            time_type=TimestampCalculation.MOST_RECENT_TIME
        )
        print(data)


Extracting summaries at regular time intervals
----------------------------------------------
