from typing import Tuple

from _voronoi import (Point as BoundPoint,
                      Segment as BoundSegment)
from hypothesis.strategies import SearchStrategy

from voronoi.point import Point as PortedPoint
from voronoi.segment import Segment as PortedSegment

Strategy = SearchStrategy

BoundPoint = BoundPoint
BoundSegment = BoundSegment

PortedPoint = PortedPoint
PortedSegment = PortedSegment

BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_segments_equal(bound: BoundSegment,
                                    ported: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end))


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_segments_pair(starts_pair: BoundPortedPointsPair,
                                       ends_pair: BoundPortedPointsPair
                                       ) -> BoundPortedSegmentsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    return (BoundSegment(bound_start, bound_end),
            PortedSegment(ported_start, ported_end))
