"""Mirror of the OSISoft.AF.Asset namespace."""

import dataclasses
from typing import Generic, Self, TypeVar, overload

import pandas as pd  # type: ignore

import PIconnect._typing.AF as _AFtyping
from PIconnect import PI, Data, _collections, dotnet

__all__ = [
    "AFDataReference",
    "AFAttribute",
    "AFAttributeList",
]

T = TypeVar("T")
ElementType = TypeVar("ElementType", bound=dotnet.AF.Asset.AFBaseElement)


@dataclasses.dataclass
class AFDataReference:
    """Reference to the data source of an AF attribute."""

    data_reference: dotnet.AF.Asset.AFDataReference

    @property
    def attribute(self) -> "AFAttribute":
        """Return the attribute associated with the data reference."""
        return AFAttribute(self.data_reference.Attribute)

    @property
    def name(self) -> str:
        """Return the name of the data reference."""
        return self.data_reference.Name

    @property
    def pi_point(self) -> PI.PIPoint | None:
        """Return the PI Point associated with the data reference, if any."""
        if self.data_reference.PIPoint is not None:
            return PI.PIPoint(self.data_reference.PIPoint)


class AFEnumerationValue:
    """Representation of an AF enumeration value."""

    def __init__(self, value: dotnet.AF.Asset.AFEnumerationValue) -> None:
        self._value = value

    def __str__(self) -> str:
        """Return the string representation of the enumeration value."""
        return self._value.Name

    def __int__(self) -> int:
        """Return the integer representation of the enumeration value."""
        return self._value.Value

    def __repr__(self):
        """Return the string representation of the enumeration value."""
        return f"{self.__class__.__qualname__}({self._value.Name})"

    @property
    def name(self) -> str:
        """Return the name of the enumeration value."""
        return self._value.Name

    @property
    def value(self) -> int:
        """Return the integer value of the enumeration value."""
        return self._value.Value

    @overload
    @staticmethod
    def wrap_enumeration_value(
        value: dotnet.AF.Asset.AFEnumerationValue,
    ) -> "AFEnumerationValue": ...
    @overload
    @staticmethod
    def wrap_enumeration_value(
        value: T,
    ) -> T: ...
    @staticmethod
    def wrap_enumeration_value(
        value: T | dotnet.AF.Asset.AFEnumerationValue,
    ) -> "T | AFEnumerationValue":
        """Wrap the value in an AFEnumerationValue if it is an enumeration value."""
        if isinstance(value, dotnet.lib.AF.Asset.AFEnumerationValue):
            return AFEnumerationValue(value)
        return value


class AFAttribute(Data.DataContainer):
    """Representation of an AF attribute."""

    def __init__(self, attribute: dotnet.AF.Asset.AFAttribute) -> None:
        super().__init__()
        self.attribute = attribute

    def __repr__(self):
        """Return the string representation of the current attribute."""
        description = ", ".join([x for x in [self.name, self.description] if x])
        value = " ".join(
            [str(x) for x in [self.current_value, self.units_of_measurement] if x]
        )
        return f"{self.__class__.__qualname__}({description}; Current Value: {value})"

    @property
    def stepped_data(self) -> bool:
        """Return True if the attribute is a stepped data type."""
        return self.attribute.Step

    @property
    def element(self) -> dotnet.AF.Asset.AFBaseElement:
        """Return the element to which the attribute belongs."""
        return self.attribute.Element

    @property
    def parent(self) -> Self | None:
        """Return the parent attribute of the current attribute, or None if it has none."""
        if not self.attribute.Parent:
            return None
        return self.__class__(self.attribute.Parent)

    @property
    def children(self) -> dict[str, Self]:
        """Return a dictionary of the direct child attributes of the current attribute."""
        return {a.Name: self.__class__(a) for a in self.attribute.Attributes}

    @property
    def path(self) -> str:
        """Return the path of the attribute."""
        return self.attribute.GetPath()

    @property
    def name(self) -> str:
        """Return the name of the attribute."""
        return self.path.split("\\")[-1]

    @property
    def data_reference(self) -> AFDataReference:
        """Return the data reference of the attribute."""
        return AFDataReference(self.attribute.DataReference)

    @property
    def description(self) -> str:
        """Return the description of the attribute."""
        return self.attribute.Description

    @property
    def units_of_measurement(self) -> str:
        """Return the units of measurement of the attribute."""
        return str(self.attribute.DefaultUOM or "")

    def _normalize_filter_expression(self, filter_expression: str) -> str:
        return super()._normalize_filter_expression(
            filter_expression.replace("%attribute%", f"'{self.attribute.Name}'")
        )

    def _current_value(self) -> object:
        """Return the current value of the attribute."""
        return AFEnumerationValue.wrap_enumeration_value(self.attribute.GetValue().Value)

    def _filtered_summaries(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        filter_expression: str,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        filter_evaluation: dotnet.AF.Data.AFSampleType,
        filter_interval: dotnet.AF.Time.AFTimeSpan,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.attribute.Data.FilteredSummaries(
            time_range,
            interval,
            filter_expression,
            summary_types,
            calculation_basis,
            filter_evaluation,
            filter_interval,
            time_type,
        )

    def _interpolated_value(self, time: dotnet.AF.Time.AFTime):
        """Return a single value for this PI Point."""
        return self.attribute.Data.InterpolatedValue(time, self.attribute.DefaultUOM)

    def _recorded_value(
        self, time: dotnet.AF.Time.AFTime, retrieval_mode: dotnet.AF.Data.AFRetrievalMode
    ) -> dotnet.AF.Asset.AFValue:
        """Return a single value for this PI Point."""
        return self.attribute.Data.RecordedValue(
            time, retrieval_mode, self.attribute.DefaultUOM
        )

    def _recorded_values(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        boundary_type: dotnet.AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> dotnet.AF.Asset.AFValues:
        include_filtered_values = False
        return self.attribute.Data.RecordedValues(
            time_range,
            boundary_type,
            self.attribute.DefaultUOM,
            filter_expression,
            include_filtered_values,
        )

    def _interpolated_values(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> dotnet.AF.Asset.AFValues:
        """Query the pi af attribute, internal implementation."""
        include_filtered_values = False
        return self.attribute.Data.InterpolatedValues(
            time_range,
            interval,
            self.attribute.DefaultUOM,
            filter_expression,
            include_filtered_values,
        )

    def _summaries(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.attribute.Data.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _summary(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        return self.attribute.Data.Summary(
            time_range, summary_types, calculation_basis, time_type
        )

    def _update_value(
        self,
        value: dotnet.AF.Asset.AFValue,
        update_mode: dotnet.AF.Data.AFUpdateOption,
        buffer_mode: dotnet.AF.Data.AFBufferOption,
    ) -> None:
        return self.attribute.Data.UpdateValue(
            value,
            update_mode,
            buffer_mode,
        )


class AFAttributeList(Data.DataContainerCollection[AFAttribute]):
    """A list of AF attributes."""

    pass


class AFBaseElement(Generic[ElementType]):
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
    def attributes(self) -> dict[str, AFAttribute]:
        """Return a dictionary of the attributes of the current element."""
        return {a.Name: AFAttribute(a) for a in self.element.Attributes}

    @property
    def categories(self) -> dotnet.AF.AFCategories:
        """Return the categories of the current element."""
        return self.element.Categories

    @property
    def description(self) -> str:
        """Return the description of the current element."""
        return self.element.Description

    @property
    def path(self) -> str:
        """Return the path of the current element."""
        return self.element.GetPath()


class AFElement(AFBaseElement[dotnet.AF.Asset.AFElement]):
    """Container for PI AF elements in the database."""

    version = "0.1.0"

    @property
    def parent(self) -> Self | None:
        """Return the parent element of the current element, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self) -> dict[str, Self]:
        """Return a dictionary of the direct child elements of the current element."""
        return {c.Name: self.__class__(c) for c in self.element.Elements}

    def descendant(self, path: str) -> Self:
        """Return a descendant of the current element from an exact path."""
        return self.__class__(self.element.Elements.get_Item(path))


class AFElementList(_collections.NamedItemList[AFElement]):
    """Container for a list of PIAFElement objects."""

    pass


class AFTable:
    """Container for PI AF Tables in the database."""

    def __init__(self, table: dotnet.AF.Asset.AFTable) -> None:
        self._table = table

    @property
    def columns(self) -> list[str]:
        """Return the names of the columns in the table."""
        return [col.ColumnName for col in self._table.Table.Columns]

    @property
    def _rows(self) -> list[dotnet.System.Data.DataRow]:
        return self._table.Table.Rows

    @property
    def name(self) -> str:
        """Return the name of the table."""
        return self._table.Name

    @property
    def shape(self) -> tuple[int, int]:
        """Return the shape of the table."""
        return (len(self._rows), len(self.columns))

    @property
    def data(self) -> pd.DataFrame:
        """Return the data in the table as a pandas DataFrame."""
        return pd.DataFrame([{col: row[col] for col in self.columns} for row in self._rows])
