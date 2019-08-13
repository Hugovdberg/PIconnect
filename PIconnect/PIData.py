"""Storage containers for PI data."""
# pragma pylint: disable=unused-import
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (
    bytes,
    dict,
    int,
    list,
    object,
    range,
    str,
    ascii,
    chr,
    hex,
    input,
    next,
    oct,
    open,
    pow,
    round,
    super,
    filter,
    map,
    zip,
)

# pragma pylint: enable=unused-import

import datetime

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABCMeta, abstractmethod

    ABC = ABCMeta(str("ABC"), (object,), {"__slots__": ()})

import pytz
from pandas import DataFrame, Series

from PIconnect.AFSDK import AF
from PIconnect.PIConsts import (
    CalculationBasis,
    ExpressionSampleType,
    SummaryType,
    TimestampCalculation,
)


class PISeries(Series):
    """Extension to pandas.Series with PI metadata."""

    version = "0.1.0"

    def __init__(self, tag, timestamp, value, uom=None, *args, **kwargs):
        Series.__init__(self, data=value, index=timestamp, name=tag, *args, **kwargs)
        self.tag = tag
        self.uom = uom

    @staticmethod
    def timestamp_to_index(timestamp):
        """Convert AFTime object to datetime.datetime in local timezone.

           TODO: Allow to define timezone, default to UTC?
        """
        local_tz = pytz.timezone("Europe/Amsterdam")
        return (
            datetime.datetime(
                timestamp.Year,
                timestamp.Month,
                timestamp.Day,
                timestamp.Hour,
                timestamp.Minute,
                timestamp.Second,
                timestamp.Millisecond * 1000,
            )
            .replace(tzinfo=pytz.utc)
            .astimezone(local_tz)
        )


class PISeriesContainer(ABC):
    """Generic class for objects that return recorded or interpolated data"""

    version = "0.1.0"

    __boundary_types = {
        "inside": AF.Data.AFBoundaryType.Inside,
        "outside": AF.Data.AFBoundaryType.Outside,
        "interpolate": AF.Data.AFBoundaryType.Interpolated,
    }

    def __init__(self):
        pass

    @abstractmethod
    def _recorded_values(self, time_range, boundary_type, filter_expression):
        """Abstract implementation for recorded values

        The internals for retrieving recorded values from PI and PI-AF are
        different and should therefore be implemented by the respective data
        containers.
        """
        pass

    @abstractmethod
    def _interpolated_values(self, time_range, interval, filter_expression):
        pass

    @abstractmethod
    def _summary(self, time_range, summary_types, calculation_basis, time_type):
        pass

    @abstractmethod
    def _summaries(
        self, time_range, interval, summary_types, calculation_basis, time_type
    ):
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def _current_value(self):
        pass

    @property
    def current_value(self):
        """Return the current value of the attribute."""
        return self._current_value()

    def recorded_values(
        self, start_time, end_time, boundary_type="inside", filter_expression=""
    ):
        """Return a PISeries of recorded data.

           Data is returned between the given *start_time* and *end_time*, inclusion
           of the boundaries is determined by the *boundary_type* attribute. Both
           *start_time* and *end_time* are parsed by AF.Time and allow for time
           specification relative to "now" by use of the asterisk.

           By default the *boundary_type* is set to 'inside', which returns from
           the first value after *start_time* to the last value before *end_time*.
           The other options are 'outside', which returns from the last value
           before *start_time* to the first value before *end_time*, and
           'interpolate', which interpolates the  first value to the given
           *start_time* and the last value to the given *end_time*.

           *filter_expression* is an optional string to filter the returned
           values, see OSIsoft PI documentation for more information.

           The AF SDK allows for inclusion of filtered data, with filtered values
           marked as such. At this point PIconnect does not support this and filtered
           values are always left out entirely.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        boundary_type = self.__boundary_types.get(boundary_type.lower())
        if boundary_type is None:
            raise ValueError(
                "Argument boundary_type must be one of "
                + ", ".join('"%s"' % x for x in sorted(self.__boundary_types.keys()))
            )
        pivalues = self._recorded_values(time_range, boundary_type, filter_expression)
        timestamps, values = [], []
        for value in pivalues:
            timestamps.append(PISeries.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        return PISeries(
            tag=self.name,
            timestamp=timestamps,
            value=values,
            uom=self.units_of_measurement,
        )

    def interpolated_values(self, start_time, end_time, interval, filter_expression=""):
        """Return a PISeries of interpolated data.

           Data is returned between *start_time* and *end_time* at a fixed
           *interval*. All three values are parsed by AF.Time and the first two
           allow for time specification relative to "now" by use of the asterisk.

           *filter_expression* is an optional string to filter the returned
           values, see OSIsoft PI documentation for more information.

           The AF SDK allows for inclusion of filtered data, with filtered values
           marked as such. At this point PIconnect does not support this and filtered
           values are always left out entirely.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        filter_expression = self._normalize_filter_expression(filter_expression)
        pivalues = self._interpolated_values(time_range, interval, filter_expression)
        timestamps, values = [], []
        for value in pivalues:
            timestamps.append(PISeries.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        return PISeries(
            tag=self.name,
            timestamp=timestamps,
            value=values,
            uom=self.units_of_measurement,
        )

    def summary(
        self,
        start_time,
        end_time,
        summary_types,
        calculation_basis=CalculationBasis.TIME_WEIGHTED,
        time_type=TimestampCalculation.AUTO,
    ):
        """Return one or more summary values over a single time range.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        summary_types = int(summary_types)
        calculation_basis = int(calculation_basis)
        time_type = int(time_type)
        pivalues = self._summary(
            time_range, summary_types, calculation_basis, time_type
        )
        df = DataFrame()
        for summary in pivalues:
            key = SummaryType(summary.Key).name
            value = summary.Value
            timestamp = PISeries.timestamp_to_index(value.Timestamp.UtcTime)
            value = value.Value
            df = df.join(DataFrame(data={key: value}, index=[timestamp]), how="outer")
        return df

    def summaries(
        self,
        start_time,
        end_time,
        interval,
        summary_types,
        calculation_basis=CalculationBasis.TIME_WEIGHTED,
        time_type=TimestampCalculation.AUTO,
    ):
        """Return one or more summary values for each interval within a time range.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        summary_types = int(summary_types)
        calculation_basis = int(calculation_basis)
        time_type = int(time_type)
        pivalues = self._summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )
        df = DataFrame()
        for summary in pivalues:
            key = SummaryType(summary.Key).name
            timestamps, values = zip(
                *[
                    (PISeries.timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ]
            )
            df = df.join(DataFrame(data={key: values}, index=timestamps), how="outer")
        return df

    def filtered_summaries(
        self,
        start_time,
        end_time,
        interval,
        filter_expression,
        summary_types,
        calculation_basis=CalculationBasis.TIME_WEIGHTED,
        filter_evaluation=ExpressionSampleType.EXPRESSION_RECORDED_VALUES,
        filter_interval=None,
        time_type=TimestampCalculation.AUTO,
    ):
        """Return one or more summary values for each interval within a time range.
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        filter_expression = self._normalize_filter_expression(filter_expression)
        filter_interval = AF.Time.AFTimeSpan.Parse(filter_interval)
        pivalues = self._filtered_summaries(
            time_range,
            interval,
            filter_expression,
            summary_types,
            calculation_basis,
            filter_evaluation,
            filter_interval,
            time_type,
        )
        df = DataFrame()
        for summary in pivalues:
            key = SummaryType(summary.Key).name
            timestamps, values = zip(
                *[
                    (PISeries.timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ]
            )
            df = df.join(DataFrame(data={key: values}, index=timestamps), how="outer")
        return df

    def _normalize_filter_expression(self, filter_expression):
        return filter_expression
