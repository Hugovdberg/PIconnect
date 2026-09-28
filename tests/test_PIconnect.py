"""Assert loading library does not throw an exception."""


def test_load_library():
    """Assert loading the PIconnect library does not throw an exception."""
    import PIconnect as PI

    PI.dotnet.lib.load_test_SDK()
