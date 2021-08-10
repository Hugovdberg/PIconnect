from PIconnect._operators import OPERATORS, add_operators
from PIconnect.PIData import PISeriesContainer
from PIconnect.time import timestamp_to_index


@add_operators(
    operators=OPERATORS,
    members=["_current_value", "interpolated_values"],
    newclassname="VirtualPIAFAttribute",
    attributes=["element", "attribute"],
)
class PIAFAttribute(PISeriesContainer):
    """Container for attributes of PI AF elements in the database."""

    version = "0.1.0"

    def __init__(self, element, attribute):
        super().__init__()
        self.element = element
        self.attribute = attribute

    def __repr__(self):
        return "%s(%s, %s; Current Value: %s %s)" % (
            self.__class__.__name__,
            self.name,
            self.description,
            self.current_value,
            self.units_of_measurement,
        )

    @property
    def name(self):
        """Return the name of the current attribute."""
        return self.attribute.Name

    @property
    def parent(self):
        """Return the parent attribute of the current attribute, or None if it has none."""
        if not self.attribute.Parent:
            return None
        return self.__class__(self.element, self.attribute.Parent)

    @property
    def children(self):
        """Return a dictionary of the direct child attributes of the current attribute."""
        return {
            a.Name: self.__class__(self.element, a) for a in self.attribute.Attributes
        }

    @property
    def description(self):
        """Return the description of the PI Point."""
        return self.attribute.Description

    @property
    def last_update(self):
        """Return the time at which the current_value was last updated."""
        return timestamp_to_index(self.attribute.GetValue().Timestamp.UtcTime)

    @property
    def units_of_measurement(self):
        """Return the units of measurement in which values for this element are reported."""
        return self.attribute.DefaultUOM

    def _current_value(self):
        return self.attribute.GetValue().Value

    def _interpolated_value(self, time):
        """Return a single value for this PI Point"""
        return self.attribute.Data.InterpolatedValue(time, self.attribute.DefaultUOM)

    def _recorded_value(self, time, retrieval_mode):
        """Return a single value for this PI Point"""
        return self.attribute.Data.RecordedValue(
            time, int(retrieval_mode), self.attribute.DefaultUOM
        )

    def _recorded_values(self, time_range, boundary_type, filter_expression):
        include_filtered_values = False
        return self.attribute.Data.RecordedValues(
            time_range,
            boundary_type,
            self.attribute.DefaultUOM,
            filter_expression,
            include_filtered_values,
        )

    def _interpolated_values(self, time_range, interval, filter_expression):
        """Internal function to actually query the pi point"""
        include_filtered_values = False
        return self.attribute.Data.InterpolatedValues(
            time_range,
            interval,
            self.attribute.DefaultUOM,
            filter_expression,
            include_filtered_values,
        )

    def _summary(self, time_range, summary_types, calculation_basis, time_type):
        return self.attribute.Data.Summary(
            time_range, summary_types, calculation_basis, time_type
        )

    def _summaries(
        self, time_range, interval, summary_types, calculation_basis, time_type
    ):
        return self.attribute.Data.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _filtered_summaries(
        self,
        time_range,
        interval,
        filter_expression,
        summary_types,
        calculation_basis,
        filter_evaluation,
        filter_interval,
        time_type,
    ):
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

    def _update_value(self, value, update_mode, buffer_mode):
        return self.attribute.Data.UpdateValue(
            value,
            update_mode,
            buffer_mode,
        )
