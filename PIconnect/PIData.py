"""
PIData contains a number of auxiliary classes that define common functionality
among :class:`PIPoint` and :class:`PIAFAttribute` objects.
"""

# pragma pylint: disable=unused-import
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import (
    ascii,
    bytes,
    chr,
    dict,
    filter,
    hex,
    input,
    int,
    list,
    map,
    next,
    object,
    oct,
    open,
    pow,
    range,
    round,
    str,
    super,
    zip,
)
from datetime import datetime

# pragma pylint: enable=unused-import


try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABCMeta, abstractmethod

    from __builtin__ import str as BuiltinStr

    ABC = ABCMeta(BuiltinStr("ABC"), (object,), {"__slots__": ()})

from pandas import DataFrame, Series

from PIconnect.AFSDK import AF
from PIconnect.PIConsts import (
    BufferMode,
    CalculationBasis,
    ExpressionSampleType,
    RetrievalMode,
    SummaryType,
    TimestampCalculation,
    UpdateMode,
    get_enumerated_value,
)
from PIconnect.time import timestamp_to_index, to_af_time_range, to_af_time


class PISeries(Series):
    """PISeries

    Create a timeseries, derived from :class:`pandas.Series`

    Args:
        tag (str): Name of the new series
        timestamp (List[datetime]): List of datetime objects to
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


class PISeriesContainer(ABC):
    """PISeriesContainer

    With the ABC class we represent a general behaviour with PI Point object
    (General class for objects that return :class:`PISeries` objects).

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
    def _interpolated_value(self, time):
        pass

    @abstractmethod
    def _recorded_value(self, time, retrieval_mode):
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
    def _update_value(self, value, update_mode, buffer_mode):
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

    def interpolated_value(self, time):
        """interpolated_value

        Return a PISeries with an interpolated value at the given time

        Args:
            time (str): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :afsdk:`AF.Time.AFTime <M_OSIsoft_AF_Time_AFTime__ctor_7.htm>`.

        Returns:
            PISeries: A PISeries with a single row, with the corresponding time as
                the index
        """
        time = to_af_time(time)
        pivalue = self._interpolated_value(time)
        return PISeries(
            tag=self.name,
            value=pivalue.Value,
            timestamp=[timestamp_to_index(pivalue.Timestamp.UtcTime)],
            uom=self.units_of_measurement,
        )

    def recorded_value(self, time, retrieval_mode=RetrievalMode.AUTO):
        """recorded_value

        Return a PISeries with the recorded value at or close to the given time

        Args:
            time (str): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :afsdk:`AF.Time.AFTime <M_OSIsoft_AF_Time_AFTime__ctor_7.htm>`.
            retrieval_mode (int or :any:`PIConsts.RetrievalMode`): Flag determining
                which value to return if no value available at the exact requested
                time.

        Returns:
            PISeries: A PISeries with a single row, with the corresponding time as
                the index
        """
        time = to_af_time(time)
        pivalue = self._recorded_value(time, retrieval_mode)
        return PISeries(
            tag=self.name,
            value=pivalue.Value,
            timestamp=[timestamp_to_index(pivalue.Timestamp.UtcTime)],
            uom=self.units_of_measurement,
        )

    def update_value(
        self,
        value,
        time=None,
        update_mode=UpdateMode.NO_REPLACE,
        buffer_mode=BufferMode.BUFFER_IF_POSSIBLE,
    ):
        """Update value for existing PI object.

        Args:
            value: value type should be in cohesion with PI object or
                it will raise PIException: [-10702] STATE Not Found
            time (datetime, optional): it is not possible to set future value,
                it raises PIException: [-11046] Target Date in Future.

        You can combine update_mode and time to change already stored value.
        """

        if time:
            time = to_af_time(time)

        value = AF.Asset.AFValue(value, time)
        return self._update_value(value, int(update_mode), int(buffer_mode))

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
        'interpolate', which interpolates the first value to the given
        *start_time* and the last value to the given *end_time*.

        *filter_expression* is an optional string to filter the returned
        values, see OSIsoft PI documentation for more information.

        The AF SDK allows for inclusion of filtered data, with filtered values
        marked as such. At this point PIconnect does not support this and
        filtered values are always left out entirely.

        Args:
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            boundary_type (str, optional): Defaults to 'inside'. Key from the
                `__boundary_types` dictionary to describe how to handle the
                boundaries of the time range.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.

        Returns:
            PISeries: Timeseries of the values returned by the SDK

        Raises:
            ValueError: If the provided `boundary_type` is not a valid key a
                `ValueError` is raised.
        """

        time_range = to_af_time_range(start_time, end_time)
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
            timestamps.append(timestamp_to_index(value.Timestamp.UtcTime))
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
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            interval (str): String containing the interval at which to extract
                data. This is parsed using
                :afsdk:`AF.Time.AFTimeSpan.Parse <M_OSIsoft_AF_Time_AFTimeSpan_Parse_1.htm>`.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.

        Returns:
            PISeries: Timeseries of the values returned by the SDK
        """
        time_range = to_af_time_range(start_time, end_time)
        interval = AF.Time.AFTimeSpan.Parse(interval)
        filter_expression = self._normalize_filter_expression(filter_expression)
        pivalues = self._interpolated_values(time_range, interval, filter_expression)
        timestamps, values = [], []
        for value in pivalues:
            timestamps.append(timestamp_to_index(value.Timestamp.UtcTime))
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
        """summary

        Return one or more summary values over a single time range.

        Args:
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            summary_types (int or PIConsts.SummaryType): Type(s) of summaries
                of the data within the requested time range.
            calculation_basis (int or PIConsts.CalculationBasis, optional):
                Event weighting within an interval. See :ref:`event_weighting`
                and :any:`CalculationBasis` for more information. Defaults to
                CalculationBasis.TIME_WEIGHTED.
            time_type (int or PIConsts.TimestampCalculation, optional):
                Timestamp to return for each of the requested summaries. See
                :ref:`summary_timestamps` and :any:`TimestampCalculation` for
                more information. Defaults to TimestampCalculation.AUTO.

        Returns:
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = to_af_time_range(start_time, end_time)
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
            timestamp = timestamp_to_index(value.Timestamp.UtcTime)
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

        Args:
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            interval (str): String containing the interval at which to extract
                data. This is parsed using
                :afsdk:`AF.Time.AFTimeSpan.Parse <M_OSIsoft_AF_Time_AFTimeSpan_Parse_1.htm>`.
            summary_types (int or PIConsts.SummaryType): Type(s) of summaries
                of the data within the requested time range.
            calculation_basis (int or PIConsts.CalculationBasis, optional):
                Event weighting within an interval. See :ref:`event_weighting`
                and :any:`CalculationBasis` for more information. Defaults to
                CalculationBasis.TIME_WEIGHTED.
            time_type (int or PIConsts.TimestampCalculation, optional):
                Timestamp to return for each of the requested summaries. See
                :ref:`summary_timestamps` and :any:`TimestampCalculation` for
                more information. Defaults to TimestampCalculation.AUTO.

        Returns:
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = to_af_time_range(start_time, end_time)
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
                    (timestamp_to_index(value.Timestamp.UtcTime), value.Value)
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
        """filtered_summaries

        Return one or more summary values for each interval within a time range

        Args:
            start_time (str or datetime): String containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            end_time (str or datetime): String containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            interval (str): String containing the interval at which to extract
                data. This is parsed using
                :afsdk:`AF.Time.AFTimeSpan.Parse <M_OSIsoft_AF_Time_AFTimeSpan_Parse_1.htm>`.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.
            summary_types (int or PIConsts.SummaryType): Type(s) of summaries
                of the data within the requested time range.
            calculation_basis (int or PIConsts.CalculationBasis, optional):
                Event weighting within an interval. See :ref:`event_weighting`
                and :any:`CalculationBasis` for more information. Defaults to
                CalculationBasis.TIME_WEIGHTED.
            filter_evaluation (int or PIConsts,ExpressionSampleType, optional):
                Determines whether the filter is applied to the raw events in
                the database, of if it is applied to an interpolated series
                with a regular interval. Defaults to
                ExpressionSampleType.EXPRESSION_RECORDED_VALUES.
            filter_interval (str, optional): String containing the interval at
                which to extract apply the filter. This is parsed using
                :afsdk:`AF.Time.AFTimeSpan.Parse <M_OSIsoft_AF_Time_AFTimeSpan_Parse_1.htm>`.
            time_type (int or PIConsts.TimestampCalculation, optional):
                Timestamp to return for each of the requested summaries. See
                :ref:`summary_timestamps` and :any:`TimestampCalculation` for
                more information. Defaults to TimestampCalculation.AUTO.

        Returns:
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = to_af_time_range(start_time, end_time)
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
                    (timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ]
            )
            df = df.join(DataFrame(data={key: values}, index=timestamps), how="outer")
        return df

    def _normalize_filter_expression(self, filter_expression):
        return filter_expression
