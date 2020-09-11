from typing import Tuple

from _voronoi import Point as BoundPoint
from hypothesis.strategies import SearchStrategy

from voronoi.point import Point as PortedPoint

Strategy = SearchStrategy

BoundPoint = BoundPoint

PortedPoint = PortedPoint

BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)
