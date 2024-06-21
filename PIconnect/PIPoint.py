"""PIPoint."""

from typing import Any, Dict, Optional

import PIconnect._typing.AF as _AFtyping
from PIconnect import AF, PIData, _time


class PIPoint(PIData.PISeriesContainer):
    """Reference to a PI Point to get data and corresponding metadata from the server.

    Parameters
    ----------
        pi_point (AF.PI.PIPoint): Reference to a PIPoint as returned by the SDK
    """

    version = "0.3.0"

    def __init__(self, pi_point: AF.PI.PIPoint) -> None:
        super().__init__()
        self.pi_point = pi_point
        self.tag = pi_point.Name
        self.__attributes_loaded = False
        self.__raw_attributes = {}

    def __repr__(self):
        """Return the string representation of the PI Point."""
        return (
            f"{self.__class__.__qualname__}({self.tag}, {self.description}; "
            f"Current Value: {self.current_value} {self.units_of_measurement})"
        )

    @property
    def created(self):
        """Return the creation datetime of a point."""
        return _time.timestamp_to_index(self.raw_attributes["creationdate"])

    @property
    def description(self):
        """Return the description of the PI Point.

        .. todo::

            Add setter to alter displayed description
        """
        return self.raw_attributes["descriptor"]

    @property
    def last_update(self):
        """Return the time at which the last value for this PI Point was recorded."""
        return _time.timestamp_to_index(self.pi_point.CurrentValue().Timestamp.UtcTime)

    @property
    def name(self) -> str:
        """Return the name of the PI Point."""
        return self.tag

    @property
    def raw_attributes(self) -> Dict[str, Any]:
        """Return a dictionary of the raw attributes of the PI Point."""
        self.__load_attributes()
        return self.__raw_attributes

    @property
    def units_of_measurement(self) -> Optional[str]:
        """Return the units of measument in which values for this PI Point are reported."""
        return self.raw_attributes["engunits"]

    def __load_attributes(self) -> None:
        """Load the raw attributes of the PI Point from the server."""
        if not self.__attributes_loaded:
            self.pi_point.LoadAttributes([])
            self.__attributes_loaded = True
        self.__raw_attributes = {att.Key: att.Value for att in self.pi_point.GetAttributes([])}

    def _current_value(self) -> Any:
        """Return the last recorded value for this PI Point (internal use only)."""
        return self.pi_point.CurrentValue().Value

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
        return self.pi_point.FilteredSummaries(
            time_range,
            interval,
            filter_expression,
            summary_types,
            calculation_basis,
            filter_evaluation,
            filter_interval,
            time_type,
        )

    def _interpolated_value(self, time: AF.Time.AFTime) -> AF.Asset.AFValue:
        """Return a single value for this PI Point."""
        return self.pi_point.InterpolatedValue(time)

    def _interpolated_values(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
        include_filtered_values = False
        return self.pi_point.InterpolatedValues(
            time_range, interval, filter_expression, include_filtered_values
        )

    def _normalize_filter_expression(self, filter_expression: str) -> str:
        return filter_expression.replace("%tag%", self.tag)

    def _recorded_value(
        self, time: AF.Time.AFTime, retrieval_mode: AF.Data.AFRetrievalMode
    ) -> AF.Asset.AFValue:
        """Return a single recorded value for this PI Point."""
        return self.pi_point.RecordedValue(time, AF.Data.AFRetrievalMode(int(retrieval_mode)))

    def _recorded_values(
        self,
        time_range: AF.Time.AFTimeRange,
        boundary_type: AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
        include_filtered_values = False
        return self.pi_point.RecordedValues(
            time_range, boundary_type, filter_expression, include_filtered_values
        )

    def _summary(
        self,
        time_range: AF.Time.AFTimeRange,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        return self.pi_point.Summary(time_range, summary_types, calculation_basis, time_type)

    def _summaries(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.pi_point.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _update_value(
        self,
        value: AF.Asset.AFValue,
        update_mode: AF.Data.AFUpdateOption,
        buffer_mode: AF.Data.AFBufferOption,
    ) -> None:
        return self.pi_point.UpdateValue(value, update_mode, buffer_mode)
