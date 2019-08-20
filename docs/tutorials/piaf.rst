##############################
Connecting to a PI AF Database
##############################

To retrieve data from the PI Asset Framework, the :any:`PIAFDatabase` object
should be used. The following code connects to the default database on the
default server, and prints its server name:

.. code-block:: python

    import PIconnect as PI

    with PI.PIAFDatabase() as database:
        print(database.server_name)

The Asset Framework represents a hierarchy of elements, with attributes on the
elements. The database has a dictionary of `children`, which you can loop over
as follows:

.. code-block:: python

    import PIconnect as PI

    with PI.PIAFDatabase() as database:
        for root in database.children.values():
            print('Root element: {r}'.format(r=root))

The keys of the dictionary are the names of the elements inside. The following
snippet first gets the first key in the dictionary, and the uses that to get
the corresponding :any:`PIAFElement` from the dictionary. Then from this
element its :any:`PIAFAttribute` are extracted:

.. code-block:: python

    import PIconnect as PI

    with PI.PIAFDatabase() as database:
        key = next(iter(database.children))
        element = database.children[key]
        for attr in element.attributes:
            print(element.attributes[attr])

To get the data for the last 48 hours from a given attribute you need the
:any:`PIAFAttribute.recorded_values` method:

.. code-block:: python

    import PIconnect as PI

    with PI.PIAFDatabase() as database:
        key = next(iter(database.children))
        element = database.children[key]
        attribute = next(iter(element.attributes.values()))
        data = attribute.recorded_values('*-48h', '*')
        print(data)

.. note:: Attributes on root elements within the database might not have
          meaningful summaries. To get a better result take a look at
          :ref:`finding_descendants` below.

.. _finding_descendants:


************************************
Finding descendants in the hierarchy
************************************

Whilst it is possible to traverse the hierarchy one at a time, by using the
:any:`PIAFElement.children` dictionaries, it is also possible to get a
further descendant using the :any:`PIAFElement.descendant` method. Assuming
the database has a root element called `Plant1` with a child element `Outlet`,
the latter element could be accessed directly as follows:

.. code-block:: python

    import PIconnect as PI

    with PI.PIAFDatabase() as database:
        element = database.descendant(r'Plant1\Outlet')

.. note:: Elements in the hierarchy are separated by a single backslash `\\`,
          use either raw strings (using the `r` prefix, as in the example
          above) or escape each backslash as `\\\\\\\\`.

.. _connect_piaf_database:

****************************************
Connecting to other servers or databases
****************************************

When no arguments are passed to the :any:`PIAFDatabase` constructor, a
connection is returned to the default database on the default server. It is
possible to connect to other servers or databases, by passing the name of the
server and database as arguments to the :any:`PIAFDatabase` constructor.

.. code-block:: python

    import PIconnect as PI

    with PI.PIAFDatabase(server='ServerName', database='DatabaseName') as database:
        print(database.server_name)

.. note:: It is also possible to specify only server or database. When only
    server is specified, a connection to the default database on that server
    is returned. Similarly, when only a database is specified, the connection
    is made to that database on the default server.

A list of the available servers can be found in the
:any:`PIAFDatabase.servers` attribute. This is a dictionary, where the keys
are the server names. To get the list of server names you can use the
following code.

.. code-block:: python

    import PIconnect as PI
    print(list(PI.PIAFDatabase.servers.keys()))

.. note:: The database names are currently not loaded until a connection to
    the server is made, this will change in a future release.
