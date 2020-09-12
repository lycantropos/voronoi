from typing import (List,
                    Tuple)

from _voronoi import (Cell as BoundCell,
                      Edge as BoundEdge,
                      Point as BoundPoint,
                      Segment as BoundSegment,
                      Vertex as BoundVertex)
from hypothesis.strategies import SearchStrategy

from voronoi.cell import Cell as PortedCell
from voronoi.edge import Edge as PortedEdge
from voronoi.point import Point as PortedPoint
from voronoi.segment import Segment as PortedSegment
from voronoi.vertex import Vertex as PortedVertex

Strategy = SearchStrategy

BoundCell = BoundCell
BoundEdge = BoundEdge
BoundPoint = BoundPoint
BoundSegment = BoundSegment
BoundVertex = BoundVertex

PortedCell = PortedCell
PortedEdge = PortedEdge
PortedPoint = PortedPoint
PortedSegment = PortedSegment
PortedVertex = PortedVertex

BoundPortedCellsPair = Tuple[BoundCell, PortedCell]
BoundPortedEdgesPair = Tuple[BoundEdge, PortedEdge]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]
BoundPortedVerticesPair = Tuple[BoundVertex, PortedVertex]


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


def are_bound_ported_edges_equal(bound: BoundEdge,
                                 ported: PortedEdge) -> bool:
    return (bound.start_index == ported.start_index
            and bound.end_index == ported.end_index
            and bound.is_primary is ported.is_primary
            and bound.is_linear is ported.is_linear
            and bound.cell_index == ported.cell_index
            and bound.twin_index == ported.twin_index)


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_segments_equal(bound: BoundSegment,
                                    ported: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end))


def are_bound_ported_vertices_equal(bound: BoundVertex, ported: PortedVertex
                                    ) -> bool:
    return bound.x == ported.x and bound.y == ported.y


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


def to_bound_with_ported_edges_pair(start_index: int,
                                    end_index: int,
                                    is_primary: bool,
                                    is_linear: bool,
                                    cell_index: int,
                                    twin_index: int) -> BoundPortedEdgesPair:
    return (BoundEdge(start_index, end_index, is_primary, is_linear,
                      cell_index, twin_index),
            PortedEdge(start_index, end_index, is_primary, is_linear,
                       cell_index, twin_index))


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_segments_pair(starts_pair: BoundPortedPointsPair,
                                       ends_pair: BoundPortedPointsPair
                                       ) -> BoundPortedSegmentsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    return (BoundSegment(bound_start, bound_end),
            PortedSegment(ported_start, ported_end))


def to_bound_with_ported_vertices_pair(x: int, y: int
                                       ) -> BoundPortedVerticesPair:
    return BoundVertex(x, y), PortedVertex(x, y)
