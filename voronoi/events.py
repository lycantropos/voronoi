from math import sqrt
from typing import (Any,
                    TypeVar)

from reprit.base import generate_repr

from .big_int import BigInt
from .enums import (ComparisonResult,
                    Orientation,
                    SourceCategory)
from .point import Point
from .utils import (compare_floats,
                    safe_divide_floats,
                    to_orientation)

ULPS = 64


class CircleEvent:
    __slots__ = 'center_x', 'center_y', 'lower_x', 'is_active'

    def __init__(self,
                 center_x: float,
                 center_y: float,
                 lower_x: float,
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
    def lower_y(self) -> float:
        return self.center_y

    @property
    def x(self) -> float:
        return self.center_x

    @x.setter
    def x(self, value: float) -> None:
        self.center_x = value

    @property
    def y(self) -> float:
        return self.center_y

    @y.setter
    def y(self, value: float) -> None:
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
    def comparison_point(self) -> Point:
        return min(self.start, self.end)

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


def to_point_point_point_circle_event(first_site: SiteEvent,
                                      second_site: SiteEvent,
                                      third_site: SiteEvent,
                                      recompute_center_x: bool = True,
                                      recompute_center_y: bool = True,
                                      recompute_lower_x: bool = True
                                      ) -> CircleEvent:
    center_x = center_y = lower_x = 0.
    first_delta_x = BigInt.from_int64(first_site.start.x - second_site.start.x)
    first_delta_y = BigInt.from_int64(first_site.start.y - second_site.start.y)
    second_delta_x = BigInt.from_int64(second_site.start.x
                                       - third_site.start.x)
    second_delta_y = BigInt.from_int64(second_site.start.y
                                       - third_site.start.y)
    inverted_denominator = safe_divide_floats(
            0.5, float(first_delta_x * second_delta_y
                       - second_delta_x * first_delta_y))
    first_sum_x = BigInt.from_int64(first_site.start.x + second_site.start.x)
    first_sum_y = BigInt.from_int64(first_site.start.y + second_site.start.y)
    first_numerator = first_delta_x * first_sum_x + first_delta_y * first_sum_y
    second_sum_x = BigInt.from_int64(second_site.start.x + third_site.start.x)
    second_sum_y = BigInt.from_int64(second_site.start.y + third_site.start.y)
    second_numerator = (second_delta_x * second_sum_x
                        + second_delta_y * second_sum_y)
    if recompute_center_x or recompute_lower_x:
        center_x_numerator = (first_numerator * second_delta_y
                              - second_numerator * first_delta_y)
        center_x = float(center_x_numerator) * inverted_denominator
        if recompute_lower_x:
            third_delta_x = BigInt.from_int32(first_site.start.x
                                              - third_site.start.x)
            third_delta_y = BigInt.from_int32(first_site.start.y
                                              - third_site.start.y)
            squared_radius = ((first_delta_x * first_delta_x
                               + first_delta_y * first_delta_y)
                              * (second_delta_x * second_delta_x
                                 + second_delta_y * second_delta_y)
                              * (third_delta_x * third_delta_x
                                 + third_delta_y * third_delta_y))
            radius = sqrt(float(squared_radius))
            # if ``center_x >= 0`` then ``lower_x = center_x + r``,
            # else ``lower_x = (center_x * center_x - r * r) / (center_x - r)``
            # to guarantee epsilon relative error
            lower_x = (
                float(center_x_numerator * center_x_numerator - squared_radius)
                * inverted_denominator / (float(center_x_numerator) + radius)
                if center_x < 0
                else (center_x - radius * inverted_denominator
                      if inverted_denominator < 0
                      else center_x + radius * inverted_denominator))
    if recompute_center_y:
        center_y = (float(second_numerator * first_delta_x
                          - first_numerator * second_delta_x)
                    * inverted_denominator)
    return CircleEvent(center_x, center_y, lower_x)
