"""Configuration for PIconnect package."""


class PIConfigContainer:
    """Configuration for PIconnect package.

    This should not be instantiated directly, but accessed through the `PIConfig` object.
    """

    _default_timezone: str = ""

    def __init__(self) -> None:
        self.DEFAULT_TIMEZONE = "UTC"

    @property
    def DEFAULT_TIMEZONE(self) -> str:
        """Timezone in which values are returned."""
        return self._default_timezone

    @DEFAULT_TIMEZONE.setter
    def DEFAULT_TIMEZONE(self, value: str) -> None:
        import zoneinfo

        if value not in zoneinfo.available_timezones():
            raise ValueError("{v!r} not found in pytz.all_timezones".format(v=value))
        self._default_timezone = value


PIConfig = PIConfigContainer()
