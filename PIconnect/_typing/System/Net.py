"""Mock classes for the System.Net module."""

from .Security import SecureString


class NetworkCredential:
    def __init__(
        self, username: str, password: SecureString, domain: str | None = None
    ) -> None:
        self.UserName = username
        self.Password = password
        self.Domain = domain
