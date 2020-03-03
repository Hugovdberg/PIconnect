####################
Extracting summaries
####################


***********************************************
Extracting a summary for a single time interval
***********************************************

The PI system allows multiple types of summaries to be calculated from data.
To get the maximum value of a :class:`~PIconnect.PI.PIPoint` in the last 14
days, you would use the :any:`PIPoint.summary` method. This takes at least
three arguments, `start_time`, `end_time` and `summary_types`, as shown in
the following code:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary('*-14d', '*', SummaryType.MAXIMUM)
        print(data)

The returned `data` is a :any:`pandas.DataFrame` with the timestamps as index
and a column for each requested summary. The timestamp in this case is the
datetime at which the maximum occurred. This is more obvious when requesting
multiple summaries over the same time span:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary('*-14d', '*', SummaryType.MAXIMUM | SummaryType.MINIMUM)
        print(data)

Similarly, a :any:`PIAFAttribute` also has a :any:`PIAFAttribute.summary`
method, that works in the same way:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType

    with PI.PIAFDatabase() as database:
        key = next(iter(database.children))
        element = database.children[key]
        attribute = next(iter(element.attributes.values()))
        data = attribute.summary('*-14d', '*', SummaryType.MAXIMUM | SummaryType.MINIMUM)
        print(data)

.. note:: Attributes on root elements within the database might not have
          meaningful summaries. To get a better result take a look at
          :ref:`finding_descendants`.

.. _summary_timestamps:

Summary timestamps
==================

Since the minimum and maximum of a point never occur at the same timestamp,
the :class:`DataFrame` in the previous example will typically occur two row.
It is possible to reduce that to a single timestamp, when the time at which
the summary value occurs is of no value.

There are two possibilities for the timestamp, the beginning of the requested
time interval, or the end of the interval. Which to return is specified using
the `time_type` argument. To always return the beginning of the interval, you
should use the :any:`TimestampCalculation.EARLIEST_TIME` constant from
:any:`PIConsts`:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType, TimestampCalculation

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary(
            '*-14d',
            '*',
            SummaryType.MAXIMUM | SummaryType.MINIMUM,
            time_type=TimestampCalculation.EARLIEST_TIME
        )
        print(data)

Similarly, the :any:`TimestampCalculation.MOST_RECENT_TIME` constant always
returns the time at the end of the interval:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType, TimestampCalculation

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary(
            '*-14d',
            '*',
            SummaryType.MAXIMUM | SummaryType.MINIMUM,
            time_type=TimestampCalculation.MOST_RECENT_TIME
        )
        print(data)


.. _event_weighting:

Event weighting
===============

Summaries of multiple data points, or events, in time can be calculated in
several ways. By default each event is weighted according to the period of
time for which it is valid. This period depends on the type of data, whether
it is stepped or continuous data.

To get an unweighted summary, in which every event has equal weight, the
:any:`CalculationBasis.EVENT_WEIGHTED` constant from the :any:`PIConsts`
module should be used:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import CalculationBasis, SummaryType

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summary(
            '*-14d',
            '*',
            SummaryType.MAXIMUM | SummaryType.MINIMUM,
            calculation_basis=CalculationBasis.EVENT_WEIGHTED
        )
        print(data)


**********************************************
Extracting summaries at regular time intervals
**********************************************

Besides extracting a single summary over an entire period of time, it is also
possible to extract summaries at fixed intervals within a period of time. This
is done using the :any:`PIPoint.summaries` or :any:`PIAFAttribute.summaries`
methods. In addition to the singular :py:meth:`summary` method, this takes an
`interval` as an argument. The following code extracts the maximum value for
each hour within the last 14 days:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import SummaryType

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.summaries('*-14d', '*', '1h', SummaryType.MAXIMUM)
        print(data)

Just as the :py:meth:`summary` methods, the :py:meth:`summaries` methods
support both changing the `Event weighting`_ and `Summary timestamps`_.
