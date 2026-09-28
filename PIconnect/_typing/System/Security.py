"""Mock classes for the System.Security module."""


class SecureString:
    def __init__(self) -> None:
        self.Value = ""

    def AppendChar(self, char: str) -> None:
        self.Value += char
