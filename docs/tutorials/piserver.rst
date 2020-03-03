#########################
Connecting to a PI Server
#########################

To connect to a PI Server you need to use the :class:`~PIconnect.PI.PIServer` class.
The following code connects to the default database and prints its name.:

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer() as server:
        print(server.server_name)

The next step is to get a list of :class:`~PIconnect.PI.PIPoint` objects from the server, and
print the first ten of those:

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
:any:`pandas.Series`, and can be used for any further processing.

***************************
Connecting to other servers
***************************

By default :class:`~PIconnect.PI.PIServer` connects to the default server, as reported by the
SDK. To find out which other servers are available you can use the
:data:`~PIconnect.PI.PIServer.servers` dictionary. The keys to the dictionary
are the server names. You can get the list of server names like this:

.. code-block:: python

    import PIconnect as PI
    print(list(PI.PIServer.servers.keys()))

To explicitly connect to any of the available servers, you pass the name of
the server to the :class:`~PIconnect.PI.PIServer` constructor.

.. code-block:: python

    import PIconnect as PI

    with PI.PIServer(server='ServerName') as server:
        print(server.server_name)

.. note:: When the server name is not found in the dictionary, a warning is
    raised and a connection to the default server is returned instead.
