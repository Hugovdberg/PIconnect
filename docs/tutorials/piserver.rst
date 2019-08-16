#########################
Connecting to a PI Server
#########################

To connect to a PI Server you need to use the :any:`PIServer` class.
The following code connects to the default database and prints its name.:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        print(server.server_name)

The next step is to get a list of :any:`PIPoint` objects from the server:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')
        for point in points[:10]:
            print(point)

To get the data as stored in the archive for a given point, we can use the
:any:`PIPoint.recorded_values` method. The following snippet gets the data
recorded in the last 48 hours:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        points = server.search('*')
        data = points[0].recorded_values('*-48h', '*')
        print(data)

The resulting `data` object is essentially a decorated version of a
:class:`pandas.Series`, and can be used for any further processing.
