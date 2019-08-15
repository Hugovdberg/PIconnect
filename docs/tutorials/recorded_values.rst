==========================
Extracting recorded values
==========================

The data in the PI archives are typically compressed. To get the exact values
as they are stored in the archive, the `recorded_values` method should be
used. This is available on both :any:`PIPoint`, and :any:`PIAFAttribute`
objects. More information on the compression algortithm can be found in this
youtube video:
`OSIsoft: Exception and Compression Full Details <https://youtu.be/89hg2mme7S0>`_.

For simplicity this tutorial only uses :any:`PIPoint` objects, see the
tutorial on :doc:`PI AF</tutorials/piaf>` to find how to access
:any:`PIAFAttribute` objects.

Boundary types
--------------

The basic example takes the first :any:`PIPoint` that is returned by the
server and gets the data for the last 48 hours, by specifying the `start_time`
and `end_time` arguments to `recorded_values`::

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.recorded_values('*-48h', '*')
        print(data)

By default only the data between the `start_time` and `end_time` is returned.
It is also possible to instead return the data from the last value before
`start_time` up to and including the first value after `end_time`, by setting
the `boundary_type` to `outside`::

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.recorded_values('*-48h', '*', boundary_type='outside')
        print(data)

Finally, it is also possible to interpolate the values surrounding both
boundaries such that a value is returned exactly at the requested timestamp::

    with PI.PIServer() as server:
        points = server.search('*')[0]
        data = points.recorded_values('*-48h', '*', boundary_type='interpolate')
        print(data)


.. _filtering_values:

Filtering values
----------------

Sometimes it is desirable to exclude certain values from the returned data.
This is possible using the `filter_expression` argument of the
:any:`PIPoint.recorded_values` method. Only values matching the expression are
returned.

The simplest test is to only return values below a given value. To test if the
values of a tag called `Plant1_Flow_out` are below the value 100, you need the
`filter_expression="'Plant1_Flow_out' < 100"`. :any:`PIPoint.recorded_values`
provides a shortcut to include the tag name, by replacing `%tag%` with the
current tag name::

    import PIconnect as PI
    with PI.PIServer() as server:
        points = server.search('*')[0]
        print(points.recorded_values(
            '*-48h',
            '*',
             filter_expression="'%tag%' < 115"
        ))

Multiple tests can be combined with the keywords `and` and `or`::

    import PIconnect as PI
    with PI.PIServer() as server:
        points = server.search('*')[0]
        print(points.recorded_values(
            '*-48h',
            '*',
             filter_expression="'%tag%' > 100 and '%tag%' < 115"
        ))
