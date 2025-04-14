"""Data access and manipulation classes."""

import abc
import datetime
import enum
from collections.abc import Callable
from typing import Any, Concatenate, Literal, ParamSpec, TypeVar, cast

import pandas as pd  # type: ignore

import PIconnect._typing.AF as _AFtyping
from PIconnect import Time, _collections, dotnet


class BoundaryType(enum.IntEnum):
    """BoundaryType indicates how to handle the boundaries of a time range.

    Detailed information is available at
    :afsdk:`AF.Data.AFBoundaryType <T_OSIsoft_AF_Data_AFBoundaryType.htm>`.
    """

    #: The first value after the start time and the last value before the end time
    INSIDE = 0
    #: The last value before the start time and the first value after the end time
    OUTSIDE = 1
    #: Interpolate values to the specified start and end time
    INTERPOLATED = 2


class SummaryType(enum.IntFlag):
    """SummaryType indicates which types of summary should be calculated.

    `SummaryType`'s are `enum.IntFlag`'s and can be or'ed together to select
    multiple summary types. For example:

    >>> SummaryType.MINIMUM | SummaryType.MAXIMUM  # Returns minimum and maximum
    <SummaryType.MAXIMUM|MINIMUM: 12>

    Detailed information is available at
    :afsdk:`AF.Data.AFSummaryTypes <T_OSIsoft_AF_Data_AFSummaryTypes.htm>`.
    """

    #: No summary data
    NONE = 0
    #: A total over the time span
    TOTAL = 1
    #: Average value over the time span
    AVERAGE = 2
    #: The minimum value in the time span
    MINIMUM = 4
    #: The maximum value in the time span
    MAXIMUM = 8
    #: The range of the values (max-min) in the time span
    RANGE = 16
    #: The sample standard deviation of the values over the time span
    STD_DEV = 32
    #: The population standard deviation of the values over the time span
    POP_STD_DEV = 64
    #: The sum of the event count (when the calculation is event weighted).
    #: The sum of the event time duration (when the calculation is time weighted.)
    COUNT = 128
    #: The percentage of the data with a good value over the time range.
    #: Based on time for time weighted calculations,
    #: based on event count for event weigthed calculations.
    PERCENT_GOOD = 8192
    #: The total over the time span,
    #: with the unit of measurement that's associated with the input
    #: (or no units if not defined for the input).
    TOTAL_WITH_UOM = 16384
    #: A convenience to retrieve all summary types
    ALL = 24831
    #: A convenience to retrieve all summary types for non-numeric data
    ALL_FOR_NON_NUMERIC = 8320


class CalculationBasis(enum.IntEnum):
    """CalculationBasis indicates how values should be weighted over a time range.

    Detailed information is available at
    :afsdk:`AF.Data.AFCalculationBasis <T_OSIsoft_AF_Data_AFCalculationBasis.htm>`.
    """

    #: Each event is weighted according to the time over which it applies.
    TIME_WEIGHTED = 0
    #: Each event is weighted equally.
    EVENT_WEIGHTED = 1
    #: Each event is time weighted, but interpolation is always done as if it is
    #: continous data.
    TIME_WEIGHTED_CONTINUOUS = 2
    #: Each event is time weighted, but interpolation is always done as if it is
    #: discrete, stepped, data.
    TIME_WEIGHTED_DISCRETE = 3
    #: Each event is weighted equally, except data at the end of the interval is
    #: excluded.
    EVENT_WEIGHTED_EXCLUDE_MOST_RECENT = 4
    #: Each event is weighted equally, except data at the beginning of the interval
    #: is excluded.
    EVENT_WEIGHTED_EXCLUDE_EARLIEST = 5
    #: Each event is weighted equally, data at both boundaries of the interval are
    #: explicitly included.
    EVENT_WEIGHTED_INCLUDE_BOTH_ENDS = 6


class ExpressionSampleType(enum.IntEnum):
    """ExpressionSampleType indicates how expressions are evaluated over a time range.

    Detailed information is available at
    :afsdk:`AF.Data.AFSampleType <T_OSIsoft_AF_Data_AFSampleType.htm>`.
    """

    #: The expression is evaluated at each archive event.
    EXPRESSION_RECORDED_VALUES = 0
    #: The expression is evaluated at a sampling interval, passed as a separate argument.
    INTERVAL = 1


class TimestampCalculation(enum.IntEnum):
    """
    TimestampCalculation defines the timestamp returned for a given summary calculation.

    Detailed information is available at
    :afsdk:`AF.Data.AFTimeStampCalculation <T_OSIsoft_AF_Data_AFTimestampCalculation.htm>`.
    """

    #: The timestamp is the event time of the minimum or maximum for those summaries
    #: or the beginning of the interval otherwise.
    AUTO = 0
    #: The timestamp is always the beginning of the interval.
    EARLIEST_TIME = 1
    #: The timestamp is always the end of the interval.
    MOST_RECENT_TIME = 2


class RetrievalMode(enum.IntEnum):
    """RetrievalMode indicates which recorded value should be returned.

    Detailed information is available at
    :afsdk:`AF.Data.AFRetrievalMode <T_OSIsoft_AF_Data_AFRetrievalMode.htm>`.
    """

    #: Autmatic detection
    AUTO = 0
    #: At the exact time if available, else the first before the requested time
    AT_OR_BEFORE = 1
    #: The first before the requested time
    BEFORE = 6
    #: At the exact time if available, else the first after the requested time
    AT_OR_AFTER = 2
    #: The first after the requested time
    AFTER = 7
    #: At the exact time if available, else return an error
    EXACT = 4


class UpdateMode(enum.IntEnum):
    """Indicates how to treat duplicate values in the archive.

    Only used when supported by the Data Reference.

    Detailed information is available at
    :afsdk:`AF.Data.AFUpdateOption <T_OSIsoft_AF_Data_AFUpdateOption.htm>`
    """

    #: Add the value to the archive.
    #: If any values exist at the same time, will overwrite one of them and set its
    #: Substituted flag.
    REPLACE = 0
    #: Add the value to the archive. Any existing values at the same time are not overwritten.
    INSERT = 1
    #: Add the value to the archive only if no value exists at the same time.
    #: If a value already exists for that time, the passed value is ignored.
    NO_REPLACE = 2
    #: Replace an existing value in the archive at the specified time.
    #: If no existing value is found, the passed value is ignored.
    REPLACE_ONLY = 3
    #: Add the value to the archive without compression.
    #: If this value is written to the snapshot, the previous snapshot value will be written to
    #: the archive,
    #: without regard to compression settings.
    #: Note that if a subsequent snapshot value is written without the InsertNoCompression
    #: option,
    #: the value added with the InsertNoCompression option is still subject to compression.
    INSERT_NO_COMPRESSION = 5
    #: Remove the value from the archive if a value exists at the passed time.
    REMOVE = 6


class BufferMode(enum.IntEnum):
    """Indicates buffering option in updating values, when supported by the Data Reference.

    Detailed information is available at
    :afsdk:`AF.Data.AFBufferOption <T_OSIsoft_AF_Data_AFBufferOption.htm>`
    """

    #: Updating data reference values without buffer.
    DO_NOT_BUFFER = 0
    #: Try updating data reference values with buffer.
    #: If fails (e.g. data reference AFDataMethods does not support Buffering,
    #: or its Buffering system is not available),
    #: then try updating directly without buffer.
    BUFFER_IF_POSSIBLE = 1
    # Updating data reference values with buffer.
    BUFFER = 2


_DEFAULT_CALCULATION_BASIS = CalculationBasis.TIME_WEIGHTED
_DEFAULT_FILTER_EVALUATION = ExpressionSampleType.EXPRESSION_RECORDED_VALUES
_DEFAULT_TIMESTAMP_CALCULATION = TimestampCalculation.AUTO


class DataContainer(abc.ABC):
    """Abstract base class for data containers."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the name of the data container."""
        pass

    @property
    @abc.abstractmethod
    def stepped_data(self) -> bool:
        """Return True if the data is stepped, False if it is continuous."""
        pass

    @property
    def current_value(self) -> Any:
        """Return the current value of the attribute."""
        return self._current_value()

    @abc.abstractmethod
    def _current_value(self) -> Any:
        """Return the current value of the attribute."""
        pass

    def filtered_summaries(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        interval: Time.IntervalLike,
        filter_expression: str,
        summary_types: SummaryType,
        calculation_basis: CalculationBasis = _DEFAULT_CALCULATION_BASIS,
        filter_evaluation: ExpressionSampleType = _DEFAULT_FILTER_EVALUATION,
        filter_interval: Time.IntervalLike | None = None,
        time_type: TimestampCalculation = _DEFAULT_TIMESTAMP_CALCULATION,
    ) -> pd.DataFrame:
        """Return one or more summary values for each interval within a time range.

        Parameters
        ----------
            start_time (str or datetime): String containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            end_time (str or datetime): String containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using
                :afsdk:`AF.Time.AFTimeRange <M_OSIsoft_AF_Time_AFTimeRange__ctor_1.htm>`.
            interval (str, datetime.timedelta or pandas.Timedelta): String containing the
                interval at which to extract data. This is parsed using
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
            filter_evaluation (int or PIConsts.ExpressionSampleType, optional):
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

        Returns
        -------
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = Time.to_af_time_range(start_time, end_time)
        _interval = Time.to_af_time_span(interval)
        _filter_expression = self._normalize_filter_expression(filter_expression)
        _summary_types = dotnet.lib.AF.Data.AFSummaryTypes(int(summary_types))
        _calculation_basis = dotnet.lib.AF.Data.AFCalculationBasis(int(calculation_basis))
        _filter_evaluation = dotnet.lib.AF.Data.AFSampleType(int(filter_evaluation))
        _filter_interval = Time.to_af_time_span(filter_interval)
        _time_type = dotnet.lib.AF.Data.AFTimestampCalculation(int(time_type))
        pivalues = self._filtered_summaries(
            time_range,
            _interval,
            _filter_expression,
            _summary_types,
            _calculation_basis,
            _filter_evaluation,
            _filter_interval,
            _time_type,
        )
        df = pd.DataFrame()
        for summary in pivalues:
            key = SummaryType(int(summary.Key)).name
            timestamps, values = zip(
                *[
                    (Time.timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ],
                strict=True,
            )
            df = df.join(
                pd.DataFrame(data={key: values}, index=timestamps),  # type: ignore
                how="outer",
            )
        return df

    @abc.abstractmethod
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
        pass

    def interpolated_value(self, time: Time.TimeLike) -> pd.Series:
        """Return a pd.Series with an interpolated value at the given time.

        Parameters
        ----------
            time (str, datetime): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :ref:`Time.to_af_time`.

        Returns
        -------
            pd.Series: A pd.Series with a single row, with the corresponding time as
                the index
        """
        _time = Time.to_af_time(time)
        pivalue = self._interpolated_value(_time)
        result = pd.Series(
            data=[pivalue.Value],
            index=[Time.timestamp_to_index(pivalue.Timestamp.UtcTime)],
            name=self.name,
        )
        result.attrs["uom"] = self.units_of_measurement
        return result

    @abc.abstractmethod
    def _interpolated_value(self, time: dotnet.AF.Time.AFTime) -> dotnet.AF.Asset.AFValue:
        pass

    def interpolated_values(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        interval: Time.IntervalLike,
        filter_expression: str = "",
    ) -> pd.Series:
        """Return a pd.Series of interpolated data.

        Data is returned between *start_time* and *end_time* at a fixed
        *interval*. All three values are parsed by AF.Time and the first two
        allow for time specification relative to "now" by use of the
        asterisk.

        *filter_expression* is an optional string to filter the returned
        values, see OSIsoft PI documentation for more information.

        The AF SDK allows for inclusion of filtered data, with filtered
        values marked as such. At this point PIconnect does not support this
        and filtered values are always left out entirely.

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            interval (str, datetime.timedelta or pd.Timedelta): String containing the interval
                at which to extract data. This is parsed using :ref:`Time.to_af_time_span`.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.

        Returns
        -------
            pd.Series: Timeseries of the values returned by the SDK
        """
        time_range = Time.to_af_time_range(start_time, end_time)
        _interval = Time.to_af_time_span(interval)
        _filter_expression = self._normalize_filter_expression(filter_expression)
        pivalues = self._interpolated_values(time_range, _interval, _filter_expression)

        timestamps: list[datetime.datetime] = []
        values: list[Any] = []
        for value in pivalues:
            timestamps.append(Time.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        result = pd.Series(
            data=values,
            index=timestamps,
            name=self.name,
        )
        result.attrs["uom"] = self.units_of_measurement
        return result

    @abc.abstractmethod
    def _interpolated_values(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> dotnet.AF.Asset.AFValues:
        pass

    def _normalize_filter_expression(self, filter_expression: str) -> str:
        return filter_expression

    def recorded_value(
        self,
        time: Time.TimeLike,
        retrieval_mode: RetrievalMode = RetrievalMode.AUTO,
    ) -> pd.Series:
        """Return a pd.Series with the recorded value at or close to the given time.

        Parameters
        ----------
            time (str): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :afsdk:`AF.Time.AFTime <M_OSIsoft_AF_Time_AFTime__ctor_7.htm>`.
            retrieval_mode (int or :any:`PIConsts.RetrievalMode`): Flag determining
                which value to return if no value available at the exact requested
                time.

        Returns
        -------
            pd.Series: A pd.Series with a single row, with the corresponding time as
                the index
        """
        _time = Time.to_af_time(time)
        _retrieval_mode = dotnet.lib.AF.Data.AFRetrievalMode(int(retrieval_mode))
        pivalue = self._recorded_value(_time, _retrieval_mode)
        result = pd.Series(
            data=[pivalue.Value],
            index=[Time.timestamp_to_index(pivalue.Timestamp.UtcTime)],
            name=self.name,
        )
        result.attrs["uom"] = self.units_of_measurement
        return result

    @abc.abstractmethod
    def _recorded_value(
        self, time: dotnet.AF.Time.AFTime, retrieval_mode: dotnet.AF.Data.AFRetrievalMode
    ) -> dotnet.AF.Asset.AFValue:
        pass

    def recorded_values(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        boundary_type: BoundaryType = BoundaryType.INSIDE,
        filter_expression: str = "",
    ):
        """Return a pd.Series of recorded data.

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

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            boundary_type (BoundaryType): Specification for how to handle values near the
                specified start and end time. Defaults to `BoundaryType.INSIDE`.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.

        Returns
        -------
            pd.Series: Timeseries of the values returned by the SDK
        """
        time_range = Time.to_af_time_range(start_time, end_time)
        _boundary_type = dotnet.lib.AF.Data.AFBoundaryType(int(boundary_type))
        _filter_expression = self._normalize_filter_expression(filter_expression)

        pivalues = self._recorded_values(time_range, _boundary_type, _filter_expression)

        timestamps: list[datetime.datetime] = []
        values: list[Any] = []
        for value in pivalues:
            timestamps.append(Time.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        result = pd.Series(
            data=values,
            index=timestamps,
            name=self.name,
        )
        result.attrs["uom"] = self.units_of_measurement
        return result

    @abc.abstractmethod
    def _recorded_values(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        boundary_type: dotnet.AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> dotnet.AF.Asset.AFValues:
        """Abstract implementation for recorded values.

        The internals for retrieving recorded values from PI and PI-AF are
        different and should therefore be implemented by the respective data
        containers.
        """
        pass

    def summary(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        summary_types: SummaryType,
        calculation_basis: CalculationBasis = _DEFAULT_CALCULATION_BASIS,
        time_type: TimestampCalculation = _DEFAULT_TIMESTAMP_CALCULATION,
    ) -> pd.DataFrame:
        """Return one or more summary values over a single time range.

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            summary_types (int or SummaryType): Type(s) of summaries
                of the data within the requested time range.
            calculation_basis (int or CalculationBasis, optional):
                Event weighting within an interval. See :ref:`event_weighting`
                and :any:`CalculationBasis` for more information. Defaults to
                CalculationBasis.TIME_WEIGHTED.
            time_type (int or TimestampCalculation, optional):
                Timestamp to return for each of the requested summaries. See
                :ref:`summary_timestamps` and :any:`TimestampCalculation` for
                more information. Defaults to TimestampCalculation.AUTO.

        Returns
        -------
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = Time.to_af_time_range(start_time, end_time)
        _summary_types = dotnet.lib.AF.Data.AFSummaryTypes(int(summary_types))
        _calculation_basis = dotnet.lib.AF.Data.AFCalculationBasis(int(calculation_basis))
        _time_type = dotnet.lib.AF.Data.AFTimestampCalculation(int(time_type))
        pivalues = self._summary(time_range, _summary_types, _calculation_basis, _time_type)
        df = pd.DataFrame()
        for summary in pivalues:
            key = SummaryType(int(summary.Key)).name
            value = summary.Value
            timestamp = Time.timestamp_to_index(value.Timestamp.UtcTime)
            value = value.Value
            df = df.join(
                pd.DataFrame(data={key: value}, index=[timestamp]),  # type: ignore
                how="outer",
            )
        return df

    @abc.abstractmethod
    def _summary(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        pass

    def summaries(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        interval: Time.IntervalLike,
        summary_types: SummaryType,
        calculation_basis: CalculationBasis = _DEFAULT_CALCULATION_BASIS,
        time_type: TimestampCalculation = _DEFAULT_TIMESTAMP_CALCULATION,
    ) -> pd.DataFrame:
        """Return one or more summary values for each interval within a time range.

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            interval (str, datetime.timedelta or pd.Timedelta): String containing the interval
                at which to extract data. This is parsed using :ref:`Time.to_af_time_span`.
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

        Returns
        -------
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = Time.to_af_time_range(start_time, end_time)
        _interval = Time.to_af_time_span(interval)
        _summary_types = dotnet.lib.AF.Data.AFSummaryTypes(int(summary_types))
        _calculation_basis = dotnet.lib.AF.Data.AFCalculationBasis(int(calculation_basis))
        _time_type = dotnet.lib.AF.Data.AFTimestampCalculation(int(time_type))
        pivalues = self._summaries(
            time_range, _interval, _summary_types, _calculation_basis, _time_type
        )
        df = pd.DataFrame()
        for summary in pivalues:
            key = SummaryType(int(summary.Key)).name
            timestamps, values = zip(
                *[
                    (Time.timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ],
                strict=True,
            )
            df = df.join(
                pd.DataFrame(data={key: values}, index=timestamps),  # type: ignore
                how="outer",
            )
        return df

    @abc.abstractmethod
    def _summaries(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        pass

    @property
    @abc.abstractmethod
    def units_of_measurement(self) -> str | None:
        """Return the units of measurement of the values in the current object."""
        pass

    def update_value(
        self,
        value: Any,
        time: Time.TimeLike | None = None,
        update_mode: UpdateMode = UpdateMode.NO_REPLACE,
        buffer_mode: BufferMode = BufferMode.BUFFER_IF_POSSIBLE,
    ) -> None:
        """Update value for existing PI object.

        Parameters
        ----------
            value: value type should be in cohesion with PI object or
                it will raise PIException: [-10702] STATE Not Found
            time (datetime, optional): it is not possible to set future value,
                it raises PIException: [-11046] Target Date in Future.

        You can combine update_mode and time to change already stored value.
        """
        from . import Time as time_module

        if time is not None:
            _value = dotnet.lib.AF.Asset.AFValue(value, time_module.to_af_time(time))
        else:
            _value = dotnet.lib.AF.Asset.AFValue(value)

        _update_mode = dotnet.lib.AF.Data.AFUpdateOption(int(update_mode))
        _buffer_mode = dotnet.lib.AF.Data.AFBufferOption(int(buffer_mode))
        self._update_value(_value, _update_mode, _buffer_mode)

    @abc.abstractmethod
    def _update_value(
        self,
        value: dotnet.AF.Asset.AFValue,
        update_mode: dotnet.AF.Data.AFUpdateOption,
        buffer_mode: dotnet.AF.Data.AFBufferOption,
    ) -> None:
        pass


DataContainerType = TypeVar("DataContainerType", bound=DataContainer)
Parameters = ParamSpec("Parameters")

Align = Literal["auto", "ffill", "bfill", "nearest", "time", False]


class DataContainerCollection(_collections.NamedItemList[DataContainerType]):
    """Container for a collection of data containers."""

    @property
    def _element_type(self) -> type[DataContainerType]:
        if len(self._elements) == 0:
            return cast(type[DataContainerType], DataContainer)
        return type(self._elements[0])

    def _combine_dfs_to_df(
        self,
        func: Callable[Concatenate[DataContainerType, Parameters], pd.DataFrame | pd.Series],
        _align: Align = False,
        _add_name_to_index: bool = False,
        *args: Parameters.args,
        **kwargs: Parameters.kwargs,
    ) -> pd.DataFrame:
        """Combine the results of a function applied to each element in the collection."""

        def add_name_to_index(df: pd.DataFrame, element: DataContainerType) -> pd.DataFrame:
            if _add_name_to_index:
                return df.set_axis(  # type: ignore
                    pd.MultiIndex.from_product([[element.name], df.columns]), axis=1
                )
            return df

        def apply_func(element: DataContainerType) -> pd.DataFrame:
            result = func(element, *args, **kwargs)
            match result:
                case pd.DataFrame():
                    df = result
                case pd.Series():
                    df = result.to_frame()
            return add_name_to_index(df, element)

        def align(df: pd.DataFrame) -> pd.DataFrame:
            match _align:
                case False:
                    return df
                case "auto":
                    for col in df.columns.get_level_values(0):  # type: ignore
                        if self[str(col)].stepped_data:  # type: ignore
                            df[col] = df[col].ffill(axis=0)  # type: ignore
                        else:
                            df[col] = (
                                df[col]
                                .apply(pd.to_numeric, errors="coerce", by_row=False)  # type: ignore
                                .interpolate(method="time", axis=0)  # type: ignore
                            )
                    return df
                case "ffill":
                    return df.ffill(axis=0)  # type: ignore
                case "bfill":
                    return df.bfill(axis=0)  # type: ignore
                case "nearest":
                    return df.interpolate(method="nearest", axis=0)  # type: ignore
                case "time":
                    return df.interpolate(method="time", axis=0)  # type: ignore

        return align(
            pd.concat(
                [pd.DataFrame()] + [apply_func(e) for e in self._elements],
                axis=1,
            )
        )

    @property
    def current_value(self) -> pd.Series:
        """Return the current values of all attributes in the collection."""
        if self._elements:
            idx, value = zip(
                *[(element.name, element.current_value) for element in self._elements],
                strict=True,
            )
        else:
            idx, value = [], []
        return pd.Series(value, index=idx)

    def filtered_summaries(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        interval: Time.IntervalLike,
        filter_expression: str,
        summary_types: SummaryType,
        calculation_basis: CalculationBasis = _DEFAULT_CALCULATION_BASIS,
        filter_evaluation: ExpressionSampleType = _DEFAULT_FILTER_EVALUATION,
        filter_interval: Time.IntervalLike | None = None,
        time_type: TimestampCalculation = _DEFAULT_TIMESTAMP_CALCULATION,
        align: Align = False,
    ) -> pd.DataFrame:
        """Return one or more summary values for each interval within a time range."""
        return self._combine_dfs_to_df(
            self._element_type.filtered_summaries,
            _align=align,
            _add_name_to_index=True,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            filter_expression=filter_expression,
            summary_types=summary_types,
            calculation_basis=calculation_basis,
            filter_evaluation=filter_evaluation,
            filter_interval=filter_interval,
            time_type=time_type,
        )

    def interpolated_value(self, time: Time.TimeLike, align: Align = False) -> pd.DataFrame:
        """Return a pd.DataFrame with an interpolated value at the given time.

        .. warning::
            Relative times are evaluated for each element in the collection,
            resulting in a different time for each element. To overcome this, use
            a fixed time, for example using the datetime module:

            >>> import datetime
            >>> time = datetime.datetime.now() - datetime.timedelta(days=1)
            >>> collection.interpolated_value(time)

        Parameters
        ----------
            time (str, datetime): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :ref:`Time.to_af_time`.

        Returns
        -------
            pd.Series: A pd.Series with a single row, with the corresponding time as
                the index
        """
        return self._combine_dfs_to_df(
            self._element_type.interpolated_value, _align=align, time=time
        )

    def interpolated_values(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        interval: Time.IntervalLike,
        filter_expression: str = "",
        align: Align = False,
    ) -> pd.DataFrame:
        """Return a pd.DataFrame of interpolated data.

        Data is returned between *start_time* and *end_time* at a fixed
        *interval*. All three values are parsed by AF.Time and the first two
        allow for time specification relative to "now" by use of the
        asterisk.

        *filter_expression* is an optional string to filter the returned
        values, see OSIsoft PI documentation for more information.

        The AF SDK allows for inclusion of filtered data, with filtered
        values marked as such. At this point PIconnect does not support this
        and filtered values are always left out entirely.

        .. warning::
            Relative times are evaluated for each element in the collection,
            resulting in a different time for each element. To overcome this, use
            a fixed time, for example using the datetime module:

            >>> import datetime
            >>> time = datetime.datetime.now() - datetime.timedelta(days=1)
            >>> collection.interpolated_value(time)

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            interval (str, datetime.timedelta or pd.Timedelta): String containing the interval
                at which to extract data. This is parsed using :ref:`Time.to_af_time_span`.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.

        Returns
        -------
            pd.DataFrame: Timeseries of the values returned by the SDK
        """
        return self._combine_dfs_to_df(
            self._element_type.interpolated_values,
            _align=align,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            filter_expression=filter_expression,
        )

    def recorded_value(
        self,
        time: Time.TimeLike,
        retrieval_mode: RetrievalMode = RetrievalMode.AUTO,
        align: Align = False,
    ) -> pd.DataFrame:
        """Return a pd.Series with the recorded value at or close to the given time.

        Parameters
        ----------
            time (str): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :afsdk:`AF.Time.AFTime <M_OSIsoft_AF_Time_AFTime__ctor_7.htm>`.
            retrieval_mode (int or :any:`PIConsts.RetrievalMode`): Flag determining
                which value to return if no value available at the exact requested
                time.

        Returns
        -------
            pd.Series: A pd.Series with a single row, with the corresponding time as
                the index
        """
        return self._combine_dfs_to_df(
            self._element_type.recorded_value,
            _align=align,
            time=time,
            retrieval_mode=retrieval_mode,
        )

    def recorded_values(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        boundary_type: BoundaryType = BoundaryType.INSIDE,
        filter_expression: str = "",
        align: Align = False,
    ) -> pd.DataFrame:
        """Return a pd.Series of recorded data.

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

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            boundary_type (BoundaryType): Specification for how to handle values near the
                specified start and end time. Defaults to `BoundaryType.INSIDE`.
            filter_expression (str, optional): Defaults to ''. Query on which
                data to include in the results. See :ref:`filtering_values`
                for more information on filter queries.

        Returns
        -------
            pd.Series: Timeseries of the values returned by the SDK
        """
        return self._combine_dfs_to_df(
            self._element_type.recorded_values,
            _align=align,
            start_time=start_time,
            end_time=end_time,
            boundary_type=boundary_type,
            filter_expression=filter_expression,
        )

    def summary(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        summary_types: SummaryType,
        calculation_basis: CalculationBasis = _DEFAULT_CALCULATION_BASIS,
        time_type: TimestampCalculation = _DEFAULT_TIMESTAMP_CALCULATION,
        align: Align = False,
    ) -> pd.DataFrame:
        """Return one or more summary values over a single time range.

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            summary_types (int or SummaryType): Type(s) of summaries
                of the data within the requested time range.
            calculation_basis (int or CalculationBasis, optional):
                Event weighting within an interval. See :ref:`event_weighting`
                and :any:`CalculationBasis` for more information. Defaults to
                CalculationBasis.TIME_WEIGHTED.
            time_type (int or TimestampCalculation, optional):
                Timestamp to return for each of the requested summaries. See
                :ref:`summary_timestamps` and :any:`TimestampCalculation` for
                more information. Defaults to TimestampCalculation.AUTO.

        Returns
        -------
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        return self._combine_dfs_to_df(
            self._element_type.summary,
            _align=align,
            _add_name_to_index=True,
            start_time=start_time,
            end_time=end_time,
            summary_types=summary_types,
            calculation_basis=calculation_basis,
            time_type=time_type,
        )

    def summaries(
        self,
        start_time: Time.TimeLike,
        end_time: Time.TimeLike,
        interval: Time.IntervalLike,
        summary_types: SummaryType,
        calculation_basis: CalculationBasis = _DEFAULT_CALCULATION_BASIS,
        time_type: TimestampCalculation = _DEFAULT_TIMESTAMP_CALCULATION,
        align: Align = False,
    ) -> pd.DataFrame:
        """Return one or more summary values for each interval within a time range.

        Parameters
        ----------
            start_time (str or datetime): Containing the date, and possibly time,
                from which to retrieve the values. This is parsed, together
                with `end_time`, using :ref:`Time.to_af_time_range`.
            end_time (str or datetime): Containing the date, and possibly time,
                until which to retrieve values. This is parsed, together
                with `start_time`, using :ref:`Time.to_af_time_range`.
            interval (str, datetime.timedelta or pd.Timedelta): String containing the interval
                at which to extract data. This is parsed using :ref:`Time.to_af_time_span`.
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

        Returns
        -------
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        return self._combine_dfs_to_df(
            self._element_type.summaries,
            _align=align,
            _add_name_to_index=True,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            summary_types=summary_types,
            calculation_basis=calculation_basis,
            time_type=time_type,
        )
