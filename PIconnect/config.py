"""Configuration for PIconnect package."""


class PIConfigContainer:
    _default_timezone: str = "UTC"

    @property
    def DEFAULT_TIMEZONE(self) -> str:
        return self._default_timezone

    @DEFAULT_TIMEZONE.setter
    def DEFAULT_TIMEZONE(self, value: str) -> None:
        import pytz

        if value not in pytz.all_timezones:
            raise ValueError("{v!r} not found in pytz.all_timezones".format(v=value))
        self._default_timezone = value


PIConfig = PIConfigContainer()
