==============================
Connecting to a PI AF Database
==============================

To retrieve data from the PI Asset Framework, the :any:`PIAFDatabase` object
should be used. The following code connects to the default database on the
default server, and prints its server name::

    import PIconnect as PI
    with PI.PIAFDatabase() as database:
        print(database.server_name)

The Asset Framework represents a hierarchy of elements, with attributes on the
elements. The database has a dictionary of `children`, which you can loop over
as follows::

    with PI.PIAFDatabase() as database:
        for root in database.children.values():
            print('Root element: {r}'.format(r=root))

The keys of the dictionary are the names of the elements inside. The following
snippet first gets the first key in the dictionary, and the uses that to get
the corresponding :any:`PIAFElement` from the dictionary. Then from this
element its :any:`PIAFAttribute` are extracted::

    with PI.PIAFDatabase() as database:
        key = next(iter(database.children))
        element = database.children[key]
        for attr in element.attributes:
            print(element.attributes[attr])

To get the data for the last 48 hours from a given attribute you need the
:any:`PIAFAttribute.recorded_values` method::

    with PI.PIAFDatabase() as database:
        key = next(iter(database.children))
        element = database.children[key]
        attribute = next(iter(element.attributes.values()))
        data = attribute.recorded_values('*-48h', '*')
        print(data)
