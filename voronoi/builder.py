from typing import (List,
                    Optional)

from reprit.base import generate_repr

from .enums import SourceCategory
from .events import SiteEvent
from .point import Point
from .utils import to_unique_just_seen


class Builder:
    __slots__ = 'index', 'site_events', '_site_event_index'

    def __init__(self,
                 index: int = 0,
                 site_events: Optional[List[SiteEvent]] = None) -> None:
        self.index = index
        self.site_events = [] if site_events is None else site_events
        self._site_event_index = None

    __repr__ = generate_repr(__init__)

    @property
    def site_event_index(self) -> int:
        return (len(self.site_events)
                if self._site_event_index is None
                else self._site_event_index)

    def init_sites_queue(self) -> None:
        self.site_events.sort()
        self.site_events = to_unique_just_seen(self.site_events)
        for index, event in enumerate(self.site_events):
            event.sorted_index = index
        self._site_event_index = 0

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
