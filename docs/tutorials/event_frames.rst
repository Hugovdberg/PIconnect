#######################
Extracting event frames
#######################

Since the data in the PI archive is compressed by default, the time interval
between consecutive values is typically irregular. To get values at regular
intervals the `interpolated_values` method is used. This is available on both
:any:`PIPoint`, and :any:`PIAFAttribute` objects.

For simplicity this tutorial only uses :any:`PIPoint` objects, see the
tutorial on :doc:`PI AF</tutorials/piaf>` to find how to access
:any:`PIAFAttribute` objects.


***********
Basic usage
***********

The basic example takes the first :any:`PIPoint` that is returned by the
server and gets the data for the last hour at 5 minute intervals,
by specifying the `start_time`, `end_time`, and `interval` arguments to
:any:`PIPoint.interpolated_values`:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.interpolated_values('*-1h', '*', '5m')
        print(data)


****************
Filtering values
****************

To filter the interpolated values the same `filter_expression` syntax as for
:ref:`filtering_values` can be used.
