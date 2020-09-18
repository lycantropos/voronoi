from math import sqrt

from .enums import (ComparisonResult,
                    Orientation)
from .events import SiteEvent
from .point import Point
from .utils import (compare_floats,
                    deltas_to_orientation,
                    robust_cross_product,
                    safe_divide_floats,
                    to_orientation)


def distance_to_point_arc(site: SiteEvent, point: Point) -> float:
    dx = float(site.start.x) - float(point.x)
    dy = float(site.start.y) - float(point.y)
    # the relative error is at most 3EPS
    return safe_divide_floats(dx * dx + dy * dy, 2.0 * dx)


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


def horizontal_goes_through_right_arc_first(left_site: SiteEvent,
                                            right_site: SiteEvent,
                                            point: Point) -> bool:
    if left_site.is_segment:
        if right_site.is_segment:
            return segment_segment_horizontal_goes_through_right_arc_first(
                    left_site, right_site, point)
        else:
            return point_segment_horizontal_goes_through_right_arc_first(
                    right_site, left_site, point, True)
    elif right_site.is_segment:
        return point_segment_horizontal_goes_through_right_arc_first(
                left_site, right_site, point, False)
    else:
        return point_point_horizontal_goes_through_right_arc_first(
                left_site, right_site, point)


def point_point_horizontal_goes_through_right_arc_first(left_site: SiteEvent,
                                                        right_site: SiteEvent,
                                                        point: Point) -> bool:
    left_point, right_point = left_site.start, right_site.start
    if left_point.x > right_point.x:
        if point.y <= left_point.y:
            return False
    elif left_point.x < right_point.x:
        if point.y >= right_point.y:
            return True
    else:
        return left_point.y + right_point.y < 2 * point.y
    distance_from_left = distance_to_point_arc(left_site, point)
    distance_from_right = distance_to_point_arc(right_site, point)
    # undefined ulp range is equal to 3EPS + 3EPS <= 6ULP
    return distance_from_left < distance_from_right


def point_point_point_circle_exists(first_site: SiteEvent,
                                    second_site: SiteEvent,
                                    third_site: SiteEvent) -> bool:
    return to_orientation(first_site.start, second_site.start,
                          third_site.start) is Orientation.RIGHT


def point_point_segment_circle_exists(first_site: SiteEvent,
                                      second_site: SiteEvent,
                                      third_site: SiteEvent,
                                      segment_index: int) -> bool:
    if segment_index == 2:
        return (third_site.start != first_site.start
                or third_site.end != second_site.start)
    else:
        first_orientation = to_orientation(first_site.start, second_site.start,
                                           third_site.start)
        second_orientation = to_orientation(first_site.start,
                                            second_site.start,
                                            third_site.end)
        if segment_index == 1 and first_site.start.x >= second_site.start.x:
            return first_orientation is Orientation.RIGHT
        elif segment_index == 3 and second_site.start.x >= first_site.start.x:
            return second_orientation is Orientation.RIGHT
        else:
            return (first_orientation is Orientation.RIGHT
                    or second_orientation is Orientation.RIGHT)


def point_segment_horizontal_goes_through_right_arc_first(
        left_site: SiteEvent,
        right_site: SiteEvent,
        point: Point,
        reverse_order: bool) -> bool:
    site_point = left_site.start
    segment_start, segment_end = right_site.start, right_site.end
    if (to_orientation(segment_start, segment_end, point)
            is not Orientation.RIGHT):
        return not right_site.is_inverse
    delta_x, delta_y = (float(point.x) - float(site_point.x),
                        float(point.y) - float(site_point.y))
    a, b = (float(segment_end.x) - float(segment_start.x),
            float(segment_end.y) - float(segment_start.y))
    if right_site.is_vertical:
        if point.y < site_point.y and not reverse_order:
            return False
        elif point.y > site_point.y and reverse_order:
            return True
    else:
        if (deltas_to_orientation(segment_end.x - segment_start.x,
                                  segment_end.y - segment_start.y,
                                  point.x - site_point.x,
                                  point.y - site_point.y)
                is Orientation.LEFT):
            if not right_site.is_inverse:
                if reverse_order:
                    return True
            elif not reverse_order:
                return False
        else:
            fast_left_expr = a * (delta_y + delta_x) * (delta_y - delta_x)
            fast_right_expr = 2. * b * delta_x * delta_y
            if ((compare_floats(fast_left_expr, fast_right_expr, 4)
                 is ComparisonResult.MORE)
                    is not reverse_order):
                return reverse_order
    distance_from_left = distance_to_point_arc(left_site, point)
    distance_from_right = distance_to_segment_arc(right_site, point)
    # undefined ulp range is equal to 3EPS + 7EPS <= 10ULP.
    return (distance_from_left < distance_from_right) is not reverse_order


def segment_segment_horizontal_goes_through_right_arc_first(
        left_site: SiteEvent,
        right_site: SiteEvent,
        point: Point) -> bool:
    # handle temporary segment sites
    if left_site.sorted_index == right_site.sorted_index:
        return (to_orientation(left_site.start, left_site.end, point)
                is Orientation.LEFT)
    distance_from_left = distance_to_segment_arc(left_site, point)
    distance_from_right = distance_to_segment_arc(right_site, point)
    # undefined ulp range is equal to 7EPS + 7EPS <= 14ULP
    return distance_from_left < distance_from_right
