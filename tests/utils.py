from typing import (List,
                    Tuple)

from _voronoi import (Cell as BoundCell,
                      Point as BoundPoint,
                      Segment as BoundSegment)
from hypothesis.strategies import SearchStrategy

from voronoi.cell import Cell as PortedCell
from voronoi.point import Point as PortedPoint
from voronoi.segment import Segment as PortedSegment

Strategy = SearchStrategy

BoundCell = BoundCell
BoundPoint = BoundPoint
BoundSegment = BoundSegment

PortedCell = PortedCell
PortedPoint = PortedPoint
PortedSegment = PortedSegment

BoundPortedCellsPair = Tuple[BoundCell, PortedCell]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def are_bound_ported_cells_equal(bound: BoundCell,
                                 ported: PortedCell) -> bool:
    return (bound.index == ported.index
            and bound.site == ported.site
            and bound.contains_point is ported.contains_point
            and bound.contains_segment is ported.contains_segment
            and bound.is_open is ported.is_open
            and bound.is_degenerate is ported.is_degenerate
            and bound.vertices_indices == ported.vertices_indices
            and bound.edges_indices == ported.edges_indices
            and bound.source_category == ported.source_category)


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_segments_equal(bound: BoundSegment,
                                    ported: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end))


def to_bound_with_ported_cells_pair(index: int,
                                    site: int,
                                    contains_point: bool,
                                    contains_segment: bool,
                                    is_open: bool,
                                    is_degenerate: bool,
                                    vertices_indices: List[int],
                                    edges_indices: List[int],
                                    source_category: int
                                    ) -> BoundPortedCellsPair:
    return (BoundCell(index, site, contains_point, contains_segment, is_open,
                      is_degenerate, vertices_indices, edges_indices,
                      source_category),
            PortedCell(index, site, contains_point, contains_segment, is_open,
                       is_degenerate, vertices_indices, edges_indices,
                       source_category))


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_segments_pair(starts_pair: BoundPortedPointsPair,
                                       ends_pair: BoundPortedPointsPair
                                       ) -> BoundPortedSegmentsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    return (BoundSegment(bound_start, bound_end),
            PortedSegment(ported_start, ported_end))
