"""
PIData contains a number of auxiliary classes that define common functionality
among :class:`PIPoint` and :class:`PIAFAttribute` objects.
"""
import abc
import datetime
from typing import Any, List, Optional

import pandas as pd

import PIconnect._typing.AF as _AFtyping
from PIconnect import PIConsts, _time, AF

__all__ = [
    "PISeries",
    "PISeriesContainer",
]


class PISeries(pd.Series):  # type: ignore
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

    def __init__(
        self,
        tag: str,
        timestamp: List[datetime.datetime],
        value: List[Any],
        uom: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        pd.Series.__init__(self, data=value, index=timestamp, name=tag, *args, **kwargs)  # type: ignore
        self.tag = tag
        self.uom = uom


class PISeriesContainer(abc.ABC):
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

    @property
    def current_value(self) -> Any:
        """current_value

        Return the current value of the attribute."""
        return self._current_value()

    @abc.abstractmethod
    def _current_value(self) -> Any:
        pass

    def filtered_summaries(
        self,
        start_time: _time.TimeLike,
        end_time: _time.TimeLike,
        interval: str,
        filter_expression: str,
        summary_types: PIConsts.SummaryType,
        calculation_basis: PIConsts.CalculationBasis = PIConsts.CalculationBasis.TIME_WEIGHTED,
        filter_evaluation: PIConsts.ExpressionSampleType = PIConsts.ExpressionSampleType.EXPRESSION_RECORDED_VALUES,
        filter_interval: Optional[str] = None,
        time_type: PIConsts.TimestampCalculation = PIConsts.TimestampCalculation.AUTO,
    ) -> pd.DataFrame:
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

        Returns:
            pandas.DataFrame: Dataframe with the unique timestamps as row index
                and the summary name as column name.
        """
        time_range = _time.to_af_time_range(start_time, end_time)
        _interval = AF.Time.AFTimeSpan.Parse(interval)
        _filter_expression = self._normalize_filter_expression(filter_expression)
        _summary_types = AF.Data.AFSummaryTypes(int(summary_types))
        _calculation_basis = AF.Data.AFCalculationBasis(int(calculation_basis))
        _filter_evaluation = AF.Data.AFSampleType(int(filter_evaluation))
        _filter_interval = AF.Time.AFTimeSpan.Parse(filter_interval)
        _time_type = AF.Data.AFTimestampCalculation(int(time_type))
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
            key = PIConsts.SummaryType(int(summary.Key)).name
            timestamps, values = zip(
                *[
                    (_time.timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ]
            )
            df = df.join(  # type: ignore
                pd.DataFrame(data={key: values}, index=timestamps), how="outer"
            )
        return df

    @abc.abstractmethod
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
        pass

    def interpolated_value(self, time: _time.TimeLike) -> PISeries:
        """interpolated_value

        Return a PISeries with an interpolated value at the given time

        Args:
            time (str, datetime): String containing the date, and possibly time,
                for which to retrieve the value. This is parsed, using
                :afsdk:`AF.Time.AFTime <M_OSIsoft_AF_Time_AFTime__ctor_7.htm>`.

        Returns:
            PISeries: A PISeries with a single row, with the corresponding time as
                the index
        """
        from . import _time as time_module

        _time = time_module.to_af_time(time)
        pivalue = self._interpolated_value(_time)
        return PISeries(  # type: ignore
            tag=self.name,
            value=pivalue.Value,
            timestamp=[time_module.timestamp_to_index(pivalue.Timestamp.UtcTime)],
            uom=self.units_of_measurement,
        )

    @abc.abstractmethod
    def _interpolated_value(self, time: AF.Time.AFTime) -> AF.Asset.AFValue:
        pass

    def interpolated_values(
        self,
        start_time: _time.TimeLike,
        end_time: _time.TimeLike,
        interval: str,
        filter_expression: str = "",
    ) -> PISeries:
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
        time_range = _time.to_af_time_range(start_time, end_time)
        _interval = AF.Time.AFTimeSpan.Parse(interval)
        _filter_expression = self._normalize_filter_expression(filter_expression)
        pivalues = self._interpolated_values(time_range, _interval, _filter_expression)

        timestamps: List[datetime.datetime] = []
        values: List[Any] = []
        for value in pivalues:
            timestamps.append(_time.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        return PISeries(  # type: ignore
            tag=self.name,
            timestamp=timestamps,
            value=values,
            uom=self.units_of_measurement,
        )

    @abc.abstractmethod
    def _interpolated_values(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    def _normalize_filter_expression(self, filter_expression: str) -> str:
        return filter_expression

    def recorded_value(
        self,
        time: _time.TimeLike,
        retrieval_mode: PIConsts.RetrievalMode = PIConsts.RetrievalMode.AUTO,
    ) -> PISeries:
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
        from . import _time as time_module

        _time = time_module.to_af_time(time)
        _retrieval_mode = AF.Data.AFRetrievalMode(int(retrieval_mode))
        pivalue = self._recorded_value(_time, _retrieval_mode)
        return PISeries(  # type: ignore
            tag=self.name,
            value=pivalue.Value,
            timestamp=[time_module.timestamp_to_index(pivalue.Timestamp.UtcTime)],
            uom=self.units_of_measurement,
        )

    @abc.abstractmethod
    def _recorded_value(
        self, time: AF.Time.AFTime, retrieval_mode: AF.Data.AFRetrievalMode
    ) -> AF.Asset.AFValue:
        pass

    def recorded_values(
        self,
        start_time: _time.TimeLike,
        end_time: _time.TimeLike,
        boundary_type: str = "inside",
        filter_expression: str = "",
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

        time_range = _time.to_af_time_range(start_time, end_time)
        _boundary_type = self.__boundary_types.get(boundary_type.lower())
        if _boundary_type is None:
            raise ValueError(
                "Argument boundary_type must be one of "
                + ", ".join('"%s"' % x for x in sorted(self.__boundary_types.keys()))
            )
        _filter_expression = self._normalize_filter_expression(filter_expression)

        pivalues = self._recorded_values(time_range, _boundary_type, _filter_expression)

        timestamps: List[datetime.datetime] = []
        values: List[Any] = []
        for value in pivalues:
            timestamps.append(_time.timestamp_to_index(value.Timestamp.UtcTime))
            values.append(value.Value)
        return PISeries(  # type: ignore
            tag=self.name,
            timestamp=timestamps,
            value=values,
            uom=self.units_of_measurement,
        )

    @abc.abstractmethod
    def _recorded_values(
        self,
        time_range: AF.Time.AFTimeRange,
        boundary_type: AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> AF.Asset.AFValues:
        """Abstract implementation for recorded values

        The internals for retrieving recorded values from PI and PI-AF are
        different and should therefore be implemented by the respective data
        containers.
        """
        pass

    def summary(
        self,
        start_time: _time.TimeLike,
        end_time: _time.TimeLike,
        summary_types: PIConsts.SummaryType,
        calculation_basis: PIConsts.CalculationBasis = PIConsts.CalculationBasis.TIME_WEIGHTED,
        time_type: PIConsts.TimestampCalculation = PIConsts.TimestampCalculation.AUTO,
    ) -> pd.DataFrame:
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
        time_range = _time.to_af_time_range(start_time, end_time)
        _summary_types = AF.Data.AFSummaryTypes(int(summary_types))
        _calculation_basis = AF.Data.AFCalculationBasis(int(calculation_basis))
        _time_type = AF.Data.AFTimestampCalculation(int(time_type))
        pivalues = self._summary(
            time_range, _summary_types, _calculation_basis, _time_type
        )
        df = pd.DataFrame()
        for summary in pivalues:
            key = PIConsts.SummaryType(int(summary.Key)).name
            value = summary.Value
            timestamp = _time.timestamp_to_index(value.Timestamp.UtcTime)
            value = value.Value
            df = df.join(  # type: ignore
                pd.DataFrame(data={key: value}, index=[timestamp]), how="outer"
            )
        return df

    @abc.abstractmethod
    def _summary(
        self,
        time_range: AF.Time.AFTimeRange,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        pass

    def summaries(
        self,
        start_time: _time.TimeLike,
        end_time: _time.TimeLike,
        interval: str,
        summary_types: PIConsts.SummaryType,
        calculation_basis: PIConsts.CalculationBasis = PIConsts.CalculationBasis.TIME_WEIGHTED,
        time_type: PIConsts.TimestampCalculation = PIConsts.TimestampCalculation.AUTO,
    ) -> pd.DataFrame:
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
        time_range = _time.to_af_time_range(start_time, end_time)
        _interval = AF.Time.AFTimeSpan.Parse(interval)
        _summary_types = AF.Data.AFSummaryTypes(int(summary_types))
        _calculation_basis = AF.Data.AFCalculationBasis(int(calculation_basis))
        _time_type = AF.Data.AFTimestampCalculation(int(time_type))
        pivalues = self._summaries(
            time_range, _interval, _summary_types, _calculation_basis, _time_type
        )
        df = pd.DataFrame()
        for summary in pivalues:
            key = PIConsts.SummaryType(int(summary.Key)).name
            timestamps, values = zip(
                *[
                    (_time.timestamp_to_index(value.Timestamp.UtcTime), value.Value)
                    for value in summary.Value
                ]
            )
            df = df.join(  # type: ignore
                pd.DataFrame(data={key: values}, index=timestamps), how="outer"
            )
        return df

    @abc.abstractmethod
    def _summaries(
        self,
        time_range: AF.Time.AFTimeRange,
        interval: AF.Time.AFTimeSpan,
        summary_types: AF.Data.AFSummaryTypes,
        calculation_basis: AF.Data.AFCalculationBasis,
        time_type: AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        pass

    @property
    @abc.abstractmethod
    def units_of_measurement(self) -> Optional[str]:
        pass

    def update_value(
        self,
        value: Any,
        time: Optional[_time.TimeLike] = None,
        update_mode: PIConsts.UpdateMode = PIConsts.UpdateMode.NO_REPLACE,
        buffer_mode: PIConsts.BufferMode = PIConsts.BufferMode.BUFFER_IF_POSSIBLE,
    ) -> None:
        """Update value for existing PI object.

        Args:
            value: value type should be in cohesion with PI object or
                it will raise PIException: [-10702] STATE Not Found
            time (datetime, optional): it is not possible to set future value,
                it raises PIException: [-11046] Target Date in Future.

        You can combine update_mode and time to change already stored value.
        """
        from . import _time as time_module

        if time is not None:
            _value = AF.Asset.AFValue(value, time_module.to_af_time(time))
        else:
            _value = AF.Asset.AFValue(value)

        _update_mode = AF.Data.AFUpdateOption(int(update_mode))
        _buffer_mode = AF.Data.AFBufferOption(int(buffer_mode))
        self._update_value(_value, _update_mode, _buffer_mode)

    @abc.abstractmethod
    def _update_value(
        self,
        value: AF.Asset.AFValue,
        update_mode: AF.Data.AFUpdateOption,
        buffer_mode: AF.Data.AFBufferOption,
    ) -> None:
        pass
