"""Mock classes for the System.Net module."""

from typing import Optional

from .Security import SecureString


class NetworkCredential:
    def __init__(
        self, username: str, password: SecureString, domain: Optional[str] = None
    ) -> None:
        self.UserName = username
        self.Password = password
        self.Domain = domain
