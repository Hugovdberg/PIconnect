"""
PIData contains a number of auxiliary classes that define common functionality
among :class:`PIPoint` and :class:`PIAFAttribute` objects.
"""

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
    from __builtin__ import str as BuiltinStr
    from abc import ABCMeta, abstractmethod

    ABC = ABCMeta(BuiltinStr("ABC"), (object,), {"__slots__": ()})

import pytz
from pandas import DataFrame, Series

from PIconnect.AFSDK import AF
from PIconnect.PIConsts import (
    CalculationBasis,
    ExpressionSampleType,
    SummaryType,
    TimestampCalculation,
    get_enumerated_value,
)


class PISeries(Series):
    """PISeries

    Create a timeseries, derived from :class:`pandas.Series`

    Args:
        tag (str): Name of the new series
        timestamp (List[datetime.datetime]): List of datetime objects to
            create the new index
        value (List): List of values for the timeseries, should be equally long
            as the `timestamp` argument
        uom (str, optional): Defaults to None. Unit of measurement for the
            series

    .. todo::

        Remove class, return to either plain :class:`pandas.Series` or a
        composition where the Series is just an attribute
    """

    version = "0.1.0"

    def __init__(self, tag, timestamp, value, uom=None, *args, **kwargs):
        Series.__init__(self, data=value, index=timestamp, name=tag, *args, **kwargs)
        self.tag = tag
        self.uom = uom

    @staticmethod
    def timestamp_to_index(timestamp):
        """Convert AFTime object to datetime.datetime in local timezone.

        .. todo::

            Allow to define timezone, default to UTC?

        .. todo::

            Move outside as separate function?
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
    """PISeriesContainer

    General class for objects that return :class:`PISeries` objects

    .. todo::

        Move `__boundary_types` to PIConsts as a new enumeration
    """

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

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def units_of_measurement(self):
        pass

    @property
    def current_value(self):
        """current_value

        Return the current value of the attribute."""
        return self._current_value()

    def recorded_values(
        self, start_time, end_time, boundary_type="inside", filter_expression=""
    ):
        """recorded_values

        Return a PISeries of recorded data.

        Data is returned between the given *start_time* and *end_time*,
        inclusion of the boundaries is determined by the *boundary_type*
        attribute. Both *start_time* and *end_time* are parsed by AF.Time and
        allow for time specification relative to "now" by use of the asterisk.

        By default the *boundary_type* is set to 'inside', which returns from
        the first value after *start_time* to the last value before *end_time*.
        The other options are 'outside', which returns from the last value
        before *start_time* to the first value before *end_time*, and
        'interpolate', which interpolates the  first value to the given
        *start_time* and the last value to the given *end_time*.

        *filter_expression* is an optional string to filter the returned
        values, see OSIsoft PI documentation for more information.

        The AF SDK allows for inclusion of filtered data, with filtered values
        marked as such. At this point PIconnect does not support this and
        filtered values are always left out entirely.

        Args:
            start_time (str): String containing the date, and possibly time,
                from which to retrieve the values.
            end_time (str): String containing the date, and possibly time,
                until which to retrieve values.
            boundary_type (str, optional): Defaults to 'inside'. Key from the
                `__boundary_types` dictionary to describe how to handle the
                boundaries of the time range.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results.

        Raises:
            ValueError: If the provided `boundary_type` is not a valid key a
                `ValueError` is raised.

        Returns:
            PISeries: Timeseries of the values returned by the SDK
        """

        time_range = AF.Time.AFTimeRange(start_time, end_time)
        boundary_type = self.__boundary_types.get(boundary_type.lower())
        filter_expression = self._normalize_filter_expression(filter_expression)
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
        """interpolated_values

        Return a PISeries of interpolated data.

        Data is returned between *start_time* and *end_time* at a fixed
        *interval*. All three values are parsed by AF.Time and the first two
        allow for time specification relative to "now" by use of the
        asterisk.

        *filter_expression* is an optional string to filter the returned
        values, see OSIsoft PI documentation for more information.

        The AF SDK allows for inclusion of filtered data, with filtered
        values marked as such. At this point PIconnect does not support this
        and filtered values are always left out entirely.

        Args:
            start_time (str): String containing the date, and possibly time,
                from which to retrieve the values.
            end_time (str): String containing the date, and possibly time,
                until which to retrieve values.
            interval (str): String containing the interval at which to extract
                data.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results.

        Returns:
            PISeries: Timeseries of the values returned by the SDK
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
        """summaries

        Return one or more summary values for each interval within a time range
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
        calculation_basis=None,
        filter_evaluation=None,
        filter_interval=None,
        time_type=None,
    ):
        """
        Return one or more summary values for each interval within a time range
        """
        time_range = AF.Time.AFTimeRange(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        filter_expression = self._normalize_filter_expression(filter_expression)
        calculation_basis = get_enumerated_value(
            enumeration=CalculationBasis,
            value=calculation_basis,
            default=CalculationBasis.TIME_WEIGHTED,
        )
        filter_evaluation = get_enumerated_value(
            enumeration=ExpressionSampleType,
            value=filter_evaluation,
            default=ExpressionSampleType.EXPRESSION_RECORDED_VALUES,
        )
        time_type = get_enumerated_value(
            enumeration=TimestampCalculation,
            value=time_type,
            default=TimestampCalculation.AUTO,
        )
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
