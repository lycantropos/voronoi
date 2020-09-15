from typing import TypeVar

from reprit.base import generate_repr

from voronoi.enums import (ComparisonResult,
                           Orientation,
                           SourceCategory)
from voronoi.point import Point
from voronoi.utils import (compare_floats,
                           to_orientation)

ULPS = 64


class CircleEvent:
    __slots__ = 'center_x', 'center_y', 'lower_x', 'is_active'

    def __init__(self,
                 center_x: int,
                 center_y: int,
                 lower_x: int,
                 is_active: bool = True) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.lower_x = lower_x
        self.is_active = is_active

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'CircleEvent') -> bool:
        return (self.center_x == other.center_x
                and self.center_y == other.center_y
                and self.lower_x == other.lower_x
                and self.is_active is other.is_active
                if isinstance(other, CircleEvent)
                else NotImplemented)

    def __lt__(self, other: 'Event') -> bool:
        return ((self.lower_x, self.y) < (other.lower_x, other.y)
                if isinstance(other, CircleEvent)
                else (compare_floats(float(self.lower_x), float(other.start.x),
                                     ULPS) is ComparisonResult.LESS
                      if isinstance(other, SiteEvent)
                      else NotImplemented))

    @property
    def lower_y(self) -> int:
        return self.center_y

    @property
    def x(self) -> int:
        return self.center_x

    @x.setter
    def x(self, value: int) -> None:
        self.center_x = value

    @property
    def y(self) -> int:
        return self.center_y

    @y.setter
    def y(self, value: int) -> None:
        self.center_y = value

    def deactivate(self) -> 'CircleEvent':
        self.is_active = False
        return self


class SiteEvent:
    __slots__ = ('start', 'end', 'sorted_index', 'initial_index', 'is_inverse',
                 'source_category')

    def __init__(self,
                 start: Point,
                 end: Point,
                 sorted_index: int = 0,
                 initial_index: int = 0,
                 is_inverse: bool = False,
                 source_category: SourceCategory = SourceCategory.SINGLE_POINT
                 ) -> None:
        self.start = start
        self.end = end
        self.sorted_index = sorted_index
        self.initial_index = initial_index
        self.is_inverse = is_inverse
        self.source_category = source_category

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'SiteEvent') -> bool:
        return (self.start == other.start and self.end == other.end
                if isinstance(other, SiteEvent)
                else NotImplemented)

    def __lt__(self, other: 'Event') -> bool:
        if isinstance(other, SiteEvent):
            if self.start.x != other.start.x:
                return self.start.x < other.start.x
            elif not self.is_segment:
                if not other.is_segment:
                    return self.start.y < other.start.y
                elif other.is_vertical:
                    return self.start.y <= other.start.y
                return True
            else:
                if other.is_vertical:
                    if self.is_vertical:
                        return self.start.y < other.start.y
                    return False
                elif self.is_vertical:
                    return True
                elif self.start.y != other.start.y:
                    return self.start.y < other.start.y
                return (to_orientation(self.end, self.start, other.end)
                        is Orientation.LEFT)
        else:
            return (compare_floats(float(self.start.x), float(other.lower_x),
                                   ULPS) is ComparisonResult.LESS
                    if isinstance(other, CircleEvent)
                    else NotImplemented)

    @property
    def is_point(self) -> bool:
        return self.start == self.end

    @property
    def is_segment(self) -> bool:
        return self.start != self.end

    @property
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def inverse(self) -> 'SiteEvent':
        self.start, self.end, self.is_inverse = (self.end, self.start,
                                                 not self.is_inverse)
        return self


Event = TypeVar('Event', CircleEvent, SiteEvent)
