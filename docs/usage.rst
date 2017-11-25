=====
Usage
=====

To use PIthon in a project::

    import PIthon as PI
    with PI.PIServer() as server:
        points = server.search('*')
        for point in points:
            print point.name, point.current_value
