=====
Usage
=====

To use PIconnect in a project::

    import PIconnect as PI
    with PI.PIServer() as server:
        points = server.search('*')
        for point in points:
            print point.name, point.current_value

    with PI.PIAFDatabase() as database:
        for child in database.children:
            for attribute in child.attributes:
                print attribute.name, attribute.current_value
