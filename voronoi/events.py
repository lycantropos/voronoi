from math import (copysign,
                  inf,
                  nan,
                  sqrt)
from typing import (Any,
                    TypeVar)

from reprit.base import generate_repr

from .enums import (ComparisonResult,
                    Orientation,
                    SourceCategory)
from .point import Point
from .utils import (compare_floats,
                    robust_cross_product,
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
            elif other.is_vertical:
                return self.is_vertical and self.start.y < other.start.y
            elif self.is_vertical:
                return True
            elif self.start.y != other.start.y:
                return self.start.y < other.start.y
            else:
                return (to_orientation(self.end, self.start, other.end)
                        is Orientation.LEFT)
        else:
            return (compare_floats(float(self.start.x), float(other.lower_x),
                                   ULPS) is ComparisonResult.LESS
                    if isinstance(other, CircleEvent)
                    else NotImplemented)

    @classmethod
    def from_point(cls, point: Point,
                   *args: Any,
                   **kwargs: Any) -> 'SiteEvent':
        return cls(point, point, *args, **kwargs)

    @property
    def is_point(self) -> bool:
        return self.start == self.end

    @property
    def is_segment(self) -> bool:
        return self.start != self.end

    @property
    def is_vertical(self) -> bool:
        return are_vertical_endpoints(self.start, self.end)

    def inverse(self) -> 'SiteEvent':
        self.start, self.end, self.is_inverse = (self.end, self.start,
                                                 not self.is_inverse)
        return self


Event = TypeVar('Event', CircleEvent, SiteEvent)


def are_vertical_endpoints(start: Point, end: Point) -> bool:
    return start.x == end.x


def distance_to_point_arc(site: SiteEvent, point: Point) -> float:
    dx = float(site.start.x) - float(point.x)
    dy = float(site.start.y) - float(point.y)
    # the relative error is at most 3EPS
    numerator = dx * dx + dy * dy
    try:
        return numerator / (2.0 * dx)
    except ZeroDivisionError:
        return copysign(inf, dx) if numerator else nan


def distance_to_segment_arc(site: SiteEvent, point: Point) -> float:
    if site.is_vertical:
        return (float(site.start.x) - float(point.x)) * 0.5
    else:
        start, end = site.start, site.end
        a1 = float(end.x) - float(start.x)
        b1 = float(end.y) - float(start.y)
        k = sqrt(a1 * a1 + b1 * b1)
        # avoid subtraction while computing k
        if not b1 < 0:
            k = 1. / (b1 + k)
        else:
            k = (k - b1) / (a1 * a1)
        return k * robust_cross_product(end.x - start.x, end.y - start.y,
                                        point.x - start.x, point.y - start.y)
