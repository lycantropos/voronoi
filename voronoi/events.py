from math import sqrt
from typing import (Any,
                    TypeVar)

from reprit.base import generate_repr

from .big_int import (BigInt,
                      robust_sum_of_products_with_sqrt_pairs
                      as pairs_sum_expression,
                      robust_sum_of_products_with_sqrt_quadruplets
                      as quadruplets_sum_expression,
                      robust_sum_of_products_with_sqrt_triplets
                      as triplets_sum_expression,
                      to_second_point_segment_segment_quadruplets_expression
                      as to_quadruplets_expression)
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


def recompute_point_point_point_circle_event(circle_event: CircleEvent,
                                             first_site: SiteEvent,
                                             second_site: SiteEvent,
                                             third_site: SiteEvent,
                                             recompute_center_x: bool = True,
                                             recompute_center_y: bool = True,
                                             recompute_lower_x: bool = True
                                             ) -> None:
    first_dx = BigInt.from_int64(first_site.start.x - second_site.start.x)
    first_dy = BigInt.from_int64(first_site.start.y - second_site.start.y)
    second_dx = BigInt.from_int64(second_site.start.x - third_site.start.x)
    second_dy = BigInt.from_int64(second_site.start.y - third_site.start.y)
    inverted_denominator = safe_divide_floats(0.5,
                                              float(first_dx * second_dy
                                                    - second_dx * first_dy))
    first_sx = BigInt.from_int64(first_site.start.x + second_site.start.x)
    first_sy = BigInt.from_int64(first_site.start.y + second_site.start.y)
    second_sx = BigInt.from_int64(second_site.start.x + third_site.start.x)
    second_sy = BigInt.from_int64(second_site.start.y + third_site.start.y)
    first_numerator = first_dx * first_sx + first_dy * first_sy
    second_numerator = second_dx * second_sx + second_dy * second_sy
    if recompute_center_x or recompute_lower_x:
        center_x_numerator = (first_numerator * second_dy
                              - second_numerator * first_dy)
        center_x = circle_event.center_x = (float(center_x_numerator)
                                            * inverted_denominator)
        if recompute_lower_x:
            third_dx = BigInt.from_int32(first_site.start.x
                                         - third_site.start.x)
            third_dy = BigInt.from_int32(first_site.start.y
                                         - third_site.start.y)
            squared_radius = ((first_dx * first_dx + first_dy * first_dy)
                              * (second_dx * second_dx + second_dy * second_dy)
                              * (third_dx * third_dx + third_dy * third_dy))
            radius = sqrt(float(squared_radius))
            # if ``center_x >= 0`` then ``lower_x = center_x + r``,
            # else ``lower_x = (center_x * center_x - r * r) / (center_x - r)``
            # to guarantee epsilon relative error
            circle_event.lower_x = (
                safe_divide_floats(
                        float(center_x_numerator * center_x_numerator
                              - squared_radius) * inverted_denominator,
                        float(center_x_numerator) + radius)
                if center_x < 0
                else (center_x - radius * inverted_denominator
                      if inverted_denominator < 0
                      else center_x + radius * inverted_denominator))
    if recompute_center_y:
        circle_event.center_y = (float(second_numerator * first_dx
                                       - first_numerator * second_dx)
                                 * inverted_denominator)


def recompute_point_point_segment_circle_event(circle_event: CircleEvent,
                                               first_site: SiteEvent,
                                               second_site: SiteEvent,
                                               third_site: SiteEvent,
                                               segment_index: int,
                                               recompute_center_x: bool = True,
                                               recompute_center_y: bool = True,
                                               recompute_lower_x: bool = True
                                               ) -> None:
    segment_dx = BigInt.from_int64(third_site.end.x - third_site.start.x)
    segment_dy = BigInt.from_int64(third_site.end.y - third_site.start.y)
    segment_length = segment_dx * segment_dx + segment_dy * segment_dy
    perpendicular_x = BigInt.from_int64(second_site.start.y
                                        - first_site.start.y)
    perpendicular_y = BigInt.from_int64(first_site.start.x
                                        - second_site.start.x)
    points_sx = BigInt.from_int64(first_site.start.x + second_site.start.x)
    points_sy = BigInt.from_int64(first_site.start.y + second_site.start.y)
    signed_perpendicular_area = (perpendicular_x * segment_dy
                                 - segment_dx * perpendicular_y)
    signed_perpendicular_projection_length = (perpendicular_x * segment_dx
                                              + perpendicular_y * segment_dy)
    # signed area of parallelogram built on
    signed_first_point_area = (
            segment_dy * BigInt.from_int64(first_site.start.x
                                           - third_site.end.x)
            - segment_dx * BigInt.from_int64(first_site.start.y
                                             - third_site.end.y))
    signed_second_point_area = (
            segment_dy * BigInt.from_int64(second_site.start.x
                                           - third_site.end.x)
            - segment_dx * BigInt.from_int64(second_site.start.y
                                             - third_site.end.y))
    signed_points_area = signed_first_point_area + signed_second_point_area
    squared_perpendicular_area = (signed_perpendicular_area
                                  * signed_perpendicular_area)
    if not signed_perpendicular_projection_length:
        squared_points_area = signed_points_area * signed_points_area
        numerator = squared_perpendicular_area - squared_points_area
        determinant = signed_perpendicular_area * signed_points_area
        coefficients = (determinant * points_sx * BigInt.from_int32(2)
                        + numerator * perpendicular_x,
                        signed_perpendicular_area
                        * (squared_points_area * BigInt.from_int32(2)
                           + numerator))
        inverted_denominator = safe_divide_floats(1., float(determinant))
        if recompute_center_x:
            circle_event.center_x = (0.25 * float(coefficients[0])
                                     * inverted_denominator)
        if recompute_center_y:
            circle_event.center_y = (0.25
                                     * float((determinant * points_sy
                                              * BigInt.from_int32(2))
                                             + numerator * perpendicular_y)
                                     * inverted_denominator)
        if recompute_lower_x:
            circle_event.lower_x = safe_divide_floats(
                    0.25 * float(pairs_sum_expression(coefficients[:2],
                                                      (segment_length,
                                                       BigInt.from_int32(1))))
                    * inverted_denominator,
                    sqrt(float(segment_length)))
    else:
        squared_perpendicular_projection_length = (
                signed_perpendicular_projection_length
                * signed_perpendicular_projection_length)
        determinant = ((squared_perpendicular_area
                        + squared_perpendicular_projection_length)
                       * signed_first_point_area
                       * signed_second_point_area
                       * BigInt.from_int32(4))
        squared_inverted_denominator = 1. / float(
                signed_perpendicular_projection_length)
        squared_inverted_denominator *= squared_inverted_denominator
        if recompute_center_x or recompute_lower_x:
            coefficients = (points_sx * squared_perpendicular_projection_length
                            + (signed_perpendicular_area * signed_points_area
                               * perpendicular_x),
                            -perpendicular_x
                            if segment_index == 2
                            else perpendicular_x)
            if recompute_center_x:
                circle_event.center_x = (0.5 * float(
                        pairs_sum_expression(coefficients,
                                             (BigInt.from_int32(1),
                                              determinant)))
                                         * squared_inverted_denominator)
            if recompute_lower_x:
                circle_event.lower_x = (0.5 * float(quadruplets_sum_expression(
                        coefficients
                        + (signed_points_area
                           * (squared_perpendicular_projection_length
                              + squared_perpendicular_area),
                           -signed_perpendicular_area
                           if segment_index == 2
                           else signed_perpendicular_area),
                        (segment_length, determinant * segment_length,
                         BigInt.from_int32(1), determinant)))
                                        * squared_inverted_denominator
                                        / sqrt(float(segment_length)))
        if recompute_center_y:
            circle_event.center_y = (0.5 * float(pairs_sum_expression(
                    (points_sy * squared_perpendicular_projection_length
                     + (signed_perpendicular_area * signed_points_area
                        * perpendicular_y),
                     -perpendicular_y
                     if segment_index == 2
                     else perpendicular_y),
                    (BigInt.from_int32(1), determinant)))
                                     * squared_inverted_denominator)


def recompute_point_segment_segment_circle_event(
        circle_event: CircleEvent,
        first_site: SiteEvent,
        second_site: SiteEvent,
        third_site: SiteEvent,
        point_index: int,
        recompute_center_x: bool = True,
        recompute_center_y: bool = True,
        recompute_lower_x: bool = True) -> None:
    second_start = second_site.start
    second_end = second_site.end
    third_start = third_site.start
    third_end = third_site.end
    second_dx = BigInt.from_int64(second_end.x - second_start.x)
    second_dy = BigInt.from_int64(second_end.y - second_start.y)
    third_dx = BigInt.from_int64(third_end.x - third_start.x)
    third_dy = BigInt.from_int64(third_end.y - third_start.y)
    third_second_signed_area = second_dx * third_dy - third_dx * second_dy
    squared_second_dx = second_dx * second_dx
    squared_second_dy = second_dy * second_dy
    if third_second_signed_area:
        third_signed_area = (third_dx * BigInt.from_int32(third_end.y)
                             - third_dy * BigInt.from_int32(third_end.x))
        second_signed_area = (second_dx * BigInt.from_int32(second_start.y)
                              - second_dy * BigInt.from_int32(second_start.x))
        ix = third_dx * second_signed_area - second_dx * third_signed_area
        iy = third_dy * second_signed_area - second_dy * third_signed_area
        dx = (ix
              - third_second_signed_area
              * BigInt.from_int32(first_site.start.x))
        dy = (iy
              - third_second_signed_area
              * BigInt.from_int32(first_site.start.y))
        if dx or dy:
            sign = BigInt.from_int32((-1 if point_index == 2 else 1)
                                     * third_second_signed_area.sign)
            common_right_coefficients = (
                squared_second_dx + squared_second_dy,
                third_dx * third_dx + third_dy * third_dy,
                -second_dx * third_dx - second_dy * third_dy,
                (second_dy * dx - second_dx * dy)
                * (third_dx * dy - third_dy * dx)
                * BigInt.from_int32(-2))
            temp = float(to_quadruplets_expression(
                    (-third_dx * dx - third_dy * dy,
                     second_dx * dx + second_dy * dy,
                     sign,
                     BigInt.from_int32(0)),
                    common_right_coefficients))
            denominator = temp * float(third_second_signed_area)
            squared_length = dx * dx + dy * dy
            if recompute_center_y:
                circle_event.center_y = (float(to_quadruplets_expression(
                        (third_dy * squared_length
                         - iy * (dx * third_dx + dy * third_dy),
                         iy * (dx * second_dx + dy * second_dy)
                         - second_dy * squared_length,
                         iy * sign,
                         BigInt.from_int32(0)),
                        common_right_coefficients))
                                         / denominator)
            if recompute_center_x or recompute_lower_x:
                common_left_coefficients = (third_dx * squared_length
                                            - ix * (dx * third_dx
                                                    + dy * third_dy),
                                            ix * (dx * second_dx
                                                  + dy * second_dy)
                                            - second_dx * squared_length,
                                            ix * sign)
                if recompute_center_x:
                    circle_event.center_x = (float(to_quadruplets_expression(
                            common_left_coefficients + (BigInt.from_int32(0),),
                            common_right_coefficients))
                                             / denominator)
                if recompute_lower_x:
                    circle_event.lower_x = (float(to_quadruplets_expression(
                            common_left_coefficients
                            + (third_second_signed_area * squared_length
                               * BigInt.from_int32(-1 if temp < 0 else 1),),
                            common_right_coefficients))
                                            / denominator)
        else:
            denominator = float(third_second_signed_area)
            circle_event.center_x = circle_event.lower_x = (float(ix)
                                                            / denominator)
            circle_event.center_y = float(iy) / denominator
    else:
        denominator = 2. * float(squared_second_dx + squared_second_dy)
        dx = (second_dy * BigInt.from_int64(first_site.start.x - second_end.x)
              - second_dx * BigInt.from_int64(first_site.start.y
                                              - second_end.y))
        dy = (second_dx * BigInt.from_int64(first_site.start.y - third_start.y)
              - second_dy * BigInt.from_int64(first_site.start.x
                                              - third_start.x))
        common_right_coefficients = (dx * dy, BigInt.from_int32(1))
        if recompute_center_y:
            circle_event.center_y = safe_divide_floats(
                    float(pairs_sum_expression(
                            (second_dy * BigInt.from_int32(-2
                                                           if point_index == 2
                                                           else 2),
                             squared_second_dx
                             * BigInt.from_int64(second_end.y + third_start.y)
                             - second_dx * second_dy
                             * BigInt.from_int64(second_end.x + third_start.x
                                                 - first_site.start.x * 2)
                             + squared_second_dy
                             * BigInt.from_int64(first_site.start.y * 2)),
                            common_right_coefficients)),
                    denominator)
        if recompute_center_x or recompute_lower_x:
            common_left_coefficients = (BigInt.from_int32(-2
                                                          if point_index == 2
                                                          else 2) * second_dx,
                                        squared_second_dy
                                        * BigInt.from_int64(second_end.x
                                                            + third_start.x)
                                        - second_dx * second_dy
                                        * BigInt.from_int64(
                                                second_end.y + third_start.y
                                                - 2 * first_site.start.y)
                                        + squared_second_dx
                                        * BigInt.from_int64(
                                                2 * first_site.start.x))
            if recompute_center_x:
                circle_event.center_x = safe_divide_floats(
                        float(pairs_sum_expression(common_left_coefficients,
                                                   common_right_coefficients)),
                        denominator)
            if recompute_lower_x:
                third_start_second_end_dx = BigInt.from_int64(third_start.x
                                                              - second_end.x)
                third_start_second_end_dy = BigInt.from_int64(third_start.y
                                                              - second_end.y)
                circle_event.lower_x = safe_divide_floats(
                        float(triplets_sum_expression(
                                common_left_coefficients
                                + (abs(second_dx * third_start_second_end_dy
                                       - second_dy
                                       * third_start_second_end_dx),),
                                common_right_coefficients
                                + (squared_second_dx + squared_second_dy,))),
                        denominator)


def recompute_segment_segment_segment_circle_event(
        circle_event: CircleEvent,
        first_site: SiteEvent,
        second_site: SiteEvent,
        third_site: SiteEvent,
        recompute_center_x: bool = True,
        recompute_center_y: bool = True,
        recompute_lower_x: bool = True) -> None:
    first_dx = BigInt.from_int64(first_site.end.x - first_site.start.x)
    first_dy = BigInt.from_int64(first_site.end.y - first_site.start.y)
    second_dx = BigInt.from_int64(second_site.end.x - second_site.start.x)
    second_dy = BigInt.from_int64(second_site.end.y - second_site.start.y)
    third_dx = BigInt.from_int64(third_site.end.x - third_site.start.x)
    third_dy = BigInt.from_int64(third_site.end.y - third_site.start.y)
    segments_lengths = (first_dx * first_dx + first_dy * first_dy,
                        second_dx * second_dx + second_dy * second_dy,
                        third_dx * third_dx + third_dy * third_dy)
    denominator = float(triplets_sum_expression(
            (second_dx * third_dy - third_dx * second_dy,
             third_dx * first_dy - first_dx * third_dy,
             first_dx * second_dy - second_dx * first_dy),
            segments_lengths))
    first_signed_area = BigInt.from_int64(
            first_site.start.x * first_site.end.y
            - first_site.start.y * first_site.end.x)
    second_signed_area = BigInt.from_int64(
            second_site.start.x * second_site.end.y
            - second_site.start.y * second_site.end.x)
    third_signed_area = BigInt.from_int64(
            third_site.start.x * third_site.end.y
            - third_site.start.y * third_site.end.x)
    if recompute_center_y:
        circle_event.center_y = safe_divide_floats(
                float(triplets_sum_expression(
                        (second_dy * third_signed_area
                         - third_dy * second_signed_area,
                         third_dy * first_signed_area
                         - first_dy * third_signed_area,
                         first_dy * second_signed_area
                         - second_dy * first_signed_area),
                        segments_lengths)),
                denominator)
    if recompute_center_x or recompute_lower_x:
        common_left_coefficients = (second_dx * third_signed_area
                                    - third_dx * second_signed_area,
                                    third_dx * first_signed_area
                                    - first_dx * third_signed_area,
                                    first_dx * second_signed_area
                                    - second_dx * first_signed_area)
        if recompute_center_x:
            circle_event.center_x = safe_divide_floats(
                    float(triplets_sum_expression(common_left_coefficients,
                                                  segments_lengths)),
                    denominator)
        if recompute_lower_x:
            circle_event.lower_x = safe_divide_floats(
                    float(quadruplets_sum_expression(
                            common_left_coefficients
                            + (common_left_coefficients[0] * first_dy
                               + common_left_coefficients[1] * second_dy
                               + common_left_coefficients[2] * third_dy,),
                            segments_lengths + (BigInt.from_int32(1),))),
                    denominator)
