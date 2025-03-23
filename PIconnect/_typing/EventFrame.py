"""Mock classes for the AF.EventFrame namespace of the OSIsoft PI-AF SDK."""

import enum
from collections.abc import Iterable

from . import AF, Asset, Time


class AFEventFrameSearchMode(enum.IntEnum):
    None_ = 0
    BackwardFromStartTime = 1
    ForwardFromStartTime = 2
    BackwardFromEndTime = 3
    ForwardFromEndTime = 4
    BackwardInProgress = 5
    ForwardInProgress = 6


class AFEventFrame(Asset.AFBaseElement):
    """Mock class of the AF.EventFrame.AFEventFrame class."""

    def __init__(self, name: str, parent: "AFEventFrame | None" = None) -> None:
        self.Name = name
        self.Parent = parent
        self.EventFrames: AFEventFrames

    @staticmethod
    def FindEventFrames(
        database: "AF.AFDatabase",
        search_root: "AFEventFrame | None",
        start_time: Time.AFTime,
        start_index: int,
        max_count: int,
        search_mode: AFEventFrameSearchMode,
        name_filter: str | None = None,
        referenced_element_name_filter: str | None = None,
        element_category: "AF.AFCategory | None" = None,
        element_template: Asset.AFElementTemplate | None = None,
        search_full_hierarchy: bool = False,
        /,
    ) -> Iterable["AFEventFrame"]:
        return []


class AFEventFrames(list[AFEventFrame]):
    def __init__(self, elements: list[AFEventFrame]) -> None:
        self.Count: int
        self._values = elements
