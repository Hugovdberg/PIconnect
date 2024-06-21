"""Base element class for PI AF elements."""

from typing import Dict, Generic, TypeVar

import PIconnect.PIAFAttribute as PIattr
from PIconnect import AF

ElementType = TypeVar("ElementType", bound=AF.Asset.AFBaseElement)


class PIAFBaseElement(Generic[ElementType]):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, element: ElementType) -> None:
        self.element = element

    def __repr__(self) -> str:
        """Return the string representation of the element."""
        return f"{self.__class__.__qualname__}({self.name})"

    @property
    def name(self) -> str:
        """Return the name of the current element."""
        return self.element.Name

    @property
    def attributes(self) -> Dict[str, PIattr.PIAFAttribute]:
        """Return a dictionary of the attributes of the current element."""
        return {a.Name: PIattr.PIAFAttribute(self.element, a) for a in self.element.Attributes}

    @property
    def categories(self) -> AF.AFCategories:
        """Return the categories of the current element."""
        return self.element.Categories

    @property
    def description(self) -> str:
        """Return the description of the current element."""
        return self.element.Description
