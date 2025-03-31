"""Module for the PIAFAttribute class."""

import dataclasses
import datetime
from collections.abc import Iterator, Sequence
from typing import Any, overload

from PIconnect import AF, PIData, PIPoint, Time

from ._typing import AF as _AFtyping

__all__ = ["PIAFAttribute"]


@dataclasses.dataclass
class AFDataReference:
    attribute: AF.Asset.AFAttribute
    data_reference: AF.Asset.AFDataReference

    @property
    def name(self) -> str:
        return self.data_reference.Name

    @property
    def pi_point(self) -> PIPoint.PIPoint | None:
        if self.data_reference.PIPoint is not None:
            return PIPoint.PIPoint(self.data_reference.PIPoint)


class PIAFAttribute(PIData.PISeriesContainer):
    """Container for attributes of PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, attribute: AF.Asset.AFAttribute) -> None:
        super().__init__()
        self.element = attribute.Element
        self.attribute = attribute

    def __repr__(self):
        """Return the string representation of the current attribute."""
        return (
            f"{self.__class__.__qualname__}({self.name}, {self.description}; "
            f"Current Value: {self.current_value} {self.units_of_measurement}"
        )

    @property
    def data_reference(self) -> AFDataReference:
        """Return the data reference of the current attribute."""
        return AFDataReference(self.attribute, self.attribute.DataReference)

    @property
    def name(self) -> str:
        """Return the name of the current attribute."""
        return self.attribute.Name

    @property
    def parent(self) -> "PIAFAttribute | None":
        """Return the parent attribute of the current attribute, or None if it has none."""
        if not self.attribute.Parent:
            return None
        return self.__class__(self.attribute.Parent)

    @property
    def children(self) -> dict[str, "PIAFAttribute"]:
        """Return a dictionary of the direct child attributes of the current attribute."""
        return {a.Name: self.__class__(a) for a in self.attribute.Attributes}

    @property
    def description(self) -> str:
        """Return the description of the PI Point."""
        return self.attribute.Description

    @property
    def last_update(self) -> datetime.datetime:
        """Return the time at which the current_value was last updated."""
        return Time.timestamp_to_index(self.attribute.GetValue().Timestamp.UtcTime)

    @property
    def units_of_measurement(self) -> str:
        """Return the units of measurement in which values for this element are reported."""
        return str(self.attribute.DefaultUOM)

    def _current_value(self) -> Any:
        return self.attribute.GetValue().Value

    def _filtered_summaries(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        filter_expression: str,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        filter_evaluation: AF.Data.AFSampleType,
        filter_interval: AF.Time.AFTimeSpan,
        time_type: AF.Data.AFTimestampCalculation,
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

    def _interpolated_value(self, time: AF.Time.AFTime):
        """Return a single value for this PI Point."""
        return self.attribute.Data.InterpolatedValue(time, self.attribute.DefaultUOM)

    def _recorded_value(
        self, time: AF.Time.AFTime, retrieval_mode: AF.Data.AFRetrievalMode
    ) -> AF.Asset.AFValue:
        """Return a single value for this PI Point."""
        return self.attribute.Data.RecordedValue(
            time, retrieval_mode, self.attribute.DefaultUOM
        )

    def _recorded_values(
        self,
        time_range: AF.Time.AFTimeRange,
        boundary_type: AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
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
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
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
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.attribute.Data.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _summary(
        self,
        time_range: AF.Time.AFTimeRange,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        return self.attribute.Data.Summary(
            time_range, summary_types, calculation_basis, time_type
        )

    def _update_value(
        self,
        value: AF.Asset.AFValue,
        update_mode: AF.Data.AFUpdateOption,
        buffer_mode: AF.Data.AFBufferOption,
    ) -> None:
        return self.attribute.Data.UpdateValue(
            value,
            update_mode,
            buffer_mode,
        )


class PIAFAttributeList(Sequence[PIAFAttribute]):
    def __init__(self, attributes: Sequence[PIAFAttribute]) -> None:
        self._attributes = attributes

    @overload
    def __getitem__(self, index: int | str) -> PIAFAttribute: ...
    @overload
    def __getitem__(self, index: slice) -> "PIAFAttributeList": ...
    def __getitem__(self, index: int | str | slice) -> "PIAFAttribute | PIAFAttributeList":
        """Return the attribute at the given index or the attribute with the given name."""
        match index:
            case int():
                return self._attributes[index]
            case str():
                for attr in self._attributes:
                    if attr.name == index:
                        return attr
                raise KeyError(f"Attribute {index} not found.")
            case slice():
                return PIAFAttributeList(self._attributes[index])
            case _:
                raise TypeError("Index must be an int or a string.")

    def __len__(self) -> int:
        """Return the number of attributes in the list."""
        return len(self._attributes)

    def __iter__(self) -> Iterator[PIAFAttribute]:
        """Return an iterator over the attributes in the list."""
        return iter(self._attributes)

    def __reversed__(self) -> Iterator[PIAFAttribute]:
        return reversed(self._attributes)

    def __repr__(self) -> str:
        """Return the string representation of the attribute list."""
        return f"{self.__class__.__qualname__}({len(self._attributes)} attributes)"
