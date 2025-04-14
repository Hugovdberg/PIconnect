from . import Asset


class AFDatabase:
    """Mock class of the AF.AFDatabase class."""

    def __init__(self, name: str) -> None:
        self.Name = name
        self.Elements = Asset.AFElements(
            [Asset.AFElement("TestElement"), Asset.AFElement("BaseElement")]
        )
        self.Tables = Asset.AFTables([Asset.AFTable("TestTable")])
