"""Mock classes for the AF.EventFrame namespace of the OSIsoft PI-AF SDK."""

import enum
from typing import Iterable, List, Optional

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

    def __init__(self, name: str, parent: Optional["AFEventFrame"] = None) -> None:
        self.Name = name
        self.Parent = parent
        self.EventFrames: AFEventFrames

    @staticmethod
    def FindEventFrames(
        database: "AF.AFDatabase",
        search_root: Optional["AFEventFrame"],
        start_time: Time.AFTime,
        start_index: int,
        max_count: int,
        search_mode: AFEventFrameSearchMode,
        name_filter: Optional[str] = None,
        referenced_element_name_filter: Optional[str] = None,
        element_category: Optional["AF.AFCategory"] = None,
        element_template: Optional[Asset.AFElementTemplate] = None,
        search_full_hierarchy: bool = False,
        /,
    ) -> Iterable["AFEventFrame"]:
        return []


class AFEventFrames(List[AFEventFrame]):
    def __init__(self, elements: List[AFEventFrame]) -> None:
        self.Count: int
        self._values = elements
