from PIconnect.PIAFAttribute import PIAFAttribute


class PIAFBaseElement(object):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)

    @property
    def name(self):
        """Return the name of the current element."""
        return self.element.Name

    @property
    def attributes(self):
        """Return a dictionary of the attributes of the current element."""
        return {a.Name: PIAFAttribute(self, a) for a in self.element.Attributes}

    @property
    def categories(self):
        return self.element.Categories

    @property
    def description(self):
        return self.element.Description
