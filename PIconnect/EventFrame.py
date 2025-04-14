"""Module for handling Event Frames."""

import enum
from typing import Self

from PIconnect import Asset, _collections, dotnet


class EventFrameSearchMode(enum.IntEnum):
    """EventFrameSearchMode.

    EventFrameSearchMode defines the interpretation and direction from the start time
    when searching for event frames.

    Detailed information is available at
    :afsdk:`AF.EventFrame.AFEventFrameSearchMode <T_OSIsoft_AF_EventFrame_AFEventFrameSearchMode.htm>`.
    including a graphical display of event frames that are returned for a given search
    mode.
    """  # noqa: E501

    #: Uninitialized
    NONE = 0
    #: Backward from start time, also known as starting before
    BACKWARD_FROM_START_TIME = 1
    STARTING_BEFORE = 1
    #: Forward from start time, also known as starting after
    FORWARD_FROM_START_TIME = 2
    STARTING_AFTER = 2
    #: Backward from end time, also known as ending before
    BACKWARD_FROM_END_TIME = 3
    ENDING_BEFORE = 3
    #: Forward from end time, also known as ending after
    FORWARD_FROM_END_TIME = 4
    ENDING_AFTER = 4
    #: Backward in progress, also known as starting before and in progress
    BACKWARD_IN_PROGRESS = 5
    STARTING_BEFORE_IN_PROGRESS = 5
    #: Forward in progress, also known as starting after and in progress
    FORWARD_IN_PROGRESS = 6
    STARTING_AFTER_IN_PROGRESS = 6


class AFEventFrame(Asset.AFBaseElement[dotnet.AF.EventFrame.AFEventFrame]):
    """Container for PI AF Event Frames in the database."""

    version = "0.1.0"

    @property
    def event_frame(self) -> dotnet.AF.EventFrame.AFEventFrame:
        """Return the underlying AF Event Frame object."""
        return self.element

    @property
    def parent(self) -> Self | None:
        """Return the parent element of the current event frame, or None if it has none."""
        if not self.element.Parent:
            return None
        return self.__class__(self.element.Parent)

    @property
    def children(self) -> dict[str, Self]:
        """Return a dictionary of the direct child event frames of the current event frame."""
        return {c.Name: self.__class__(c) for c in self.element.EventFrames}


class AFEventFrameList(_collections.NamedItemList[AFEventFrame]):
    """Container for a list of PIAFEventFrame objects."""

    pass
