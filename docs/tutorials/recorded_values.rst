##########################
Extracting recorded values
##########################

The data in the PI archives are typically compressed [#compression]_. To get the exact values
as they are stored in the archive, the `recorded_values` method should be
used. It is also possible to extract a single historic value using `recorded_value`.
This is available on both :class:`~PIconnect.PI.PIPoint`, and :any:`PIAFAttribute` objects.

For simplicity this tutorial only uses :class:`~PIconnect.PI.PIPoint` objects,
see the tutorial on :doc:`PI AF</tutorials/piaf>` to find how to access
:any:`PIAFAttribute` objects.

.. [#compression] More information on the compression algorithm can be found in this youtube
    video:
    `OSIsoft: Exception and Compression Full Details <https://youtu.be/89hg2mme7S0>`_.

*************************
Single vs Multiple values
*************************

We start of by extracting a the value from the first :class:`~PIconnect.PI.PIPoint`
that is returned by the server as it was 5 minutes ago.

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        point = server.search('*')[0]
        data = point.recorded_value('-5m')
        print(data)

You will see :any:`PISeries` is printed containing a single row, with the PIPoint name
as the Series name, the point value as the value, and the corresponding timestamp as
the index.

By default the PI Server automatically detects which value to select and returns it
with the requested timestamp as the index. To control which value is returned, we pass
the `retrieval_mode` argument to `recorded_value`:

.. code-block:: python

    import PIconnect as PI
    from PIconnect.PIConsts import RetrievalMode

    with PI.PIServer() as server:
        point = server.search('*')[0]
        data = point.recorded_value('-5m', retrieval_mode=RetrievalMode.AT_OR_BEFORE)
        print(data)

Since it is unlikely there is a value at exactly 5 minutes ago, the PI Server now
returns the latest value that's before the requested time. Also the index is now no
longer at the requested time, but at the time the value was recorded.

Now to get a time series of the values from the :class:`~PIconnect.PI.PIPoint` we use
the `recorded_values` method, and pass a `start_time` and `end_time`:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.recorded_values('*-48h', '*')
        print(data)

**************
Boundary types
**************

By default only the data between the `start_time` and `end_time` is returned.
It is also possible to instead return the data from the last value before
`start_time` up to and including the first value after `end_time`, by setting
the `boundary_type` to `outside`:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.recorded_values('*-48h', '*', boundary_type='outside')
        print(data)

.. warning:: The :py:data:`boundary_type` argument currently takes a string as
             the key to the internal :py:data:`__boundary_types` dictionary.
             This will change in a future version to an enumeration in
             :any:`PIConsts`.

Finally, it is also possible to interpolate the values surrounding both
boundaries such that a value is returned exactly at the requested timestamp:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.recorded_values('*-48h', '*', boundary_type='interpolate')
        print(data)


.. _filtering_values:

****************
Filtering values
****************

Sometimes it is desirable to exclude certain values from the returned data.
This is possible using the `filter_expression` argument of the
:any:`PIPoint.recorded_values` method. Only values matching the expression are
returned.

The simplest test is to only return values below a given value. To test if the
values of a tag called `Plant1_Flow_out` are below the value 100, you need the
`filter_expression="'Plant1_Flow_out' < 100"`. :any:`PIPoint.recorded_values`
provides a shortcut to include the tag name, by replacing `%tag%` with the
current tag name:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')[0]
        print(points.recorded_values(
            '*-48h',
            '*',
             filter_expression="'%tag%' < 115"
        ))

Multiple tests can be combined with the keywords `and` and `or`:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')[0]
        print(points.recorded_values(
            '*-48h',
            '*',
             filter_expression="'%tag%' > 100 and '%tag%' < 115"
        ))
