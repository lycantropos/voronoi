from typing import (List,
                    Optional)

from reprit.base import generate_repr

from .enums import SourceCategory
from .events import SiteEvent
from .point import Point


class Builder:
    __slots__ = 'index', 'site_events'

    def __init__(self,
                 index: int = 0,
                 site_events: Optional[List[SiteEvent]] = None) -> None:
        self.index = index
        self.site_events = [] if site_events is None else site_events

    __repr__ = generate_repr(__init__)

    def insert_point(self, x: int, y: int) -> int:
        index = self.index
        self.site_events.append(SiteEvent.from_point(
                Point(x, y),
                initial_index=index,
                source_category=SourceCategory.SINGLE_POINT))
        self.index += 1
        return index

    def insert_segment(self,
                       start_x: int,
                       start_y: int,
                       end_x: int,
                       end_y: int) -> int:
        site_events = self.site_events
        index = self.index
        start = Point(start_x, start_y)
        end = Point(end_x, end_y)
        site_events.append(SiteEvent.from_point(
                start,
                initial_index=index,
                source_category=SourceCategory.SEGMENT_START_POINT))
        site_events.append(SiteEvent.from_point(
                end,
                initial_index=index,
                source_category=SourceCategory.SEGMENT_END_POINT))
        site_events.append(
                SiteEvent(start, end,
                          source_category=SourceCategory.INITIAL_SEGMENT,
                          initial_index=index)
                if start < end
                else SiteEvent(end, start,
                               source_category=SourceCategory.REVERSE_SEGMENT,
                               initial_index=index))
        self.index += 1
        return index
