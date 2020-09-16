from enum import Enum
from functools import partial
from operator import is_
from typing import (Callable,
                    List,
                    Optional,
                    Tuple,
                    Type,
                    TypeVar,
                    Union)

from _voronoi import (Builder as BoundBuilder,
                      Cell as BoundCell,
                      CircleEvent as BoundCircleEvent,
                      Edge as BoundEdge,
                      GeometryCategory as BoundGeometryCategory,
                      Point as BoundPoint,
                      Segment as BoundSegment,
                      SiteEvent as BoundSiteEvent,
                      SourceCategory as BoundSourceCategory,
                      Vertex as BoundVertex)
from hypothesis import strategies
from hypothesis.strategies import SearchStrategy

from voronoi.builder import Builder as PortedBuilder
from voronoi.enums import (GeometryCategory as PortedGeometryCategory,
                           SourceCategory as PortedSourceCategory)
from voronoi.events import (CircleEvent as PortedCircleEvent,
                            SiteEvent as PortedSiteEvent)
from voronoi.faces import (Cell as PortedCell,
                           Edge as PortedEdge,
                           Vertex as PortedVertex)
from voronoi.point import Point as PortedPoint
from voronoi.segment import Segment as PortedSegment

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy

BoundBuilder = BoundBuilder
BoundCell = BoundCell
BoundCircleEvent = BoundCircleEvent
BoundEdge = BoundEdge
BoundGeometryCategory = BoundGeometryCategory
BoundPoint = BoundPoint
BoundSegment = BoundSegment
BoundSiteEvent = BoundSiteEvent
BoundSourceCategory = BoundSourceCategory
BoundVertex = BoundVertex

PortedBuilder = PortedBuilder
PortedCell = PortedCell
PortedCircleEvent = PortedCircleEvent
PortedEdge = PortedEdge
PortedGeometryCategory = PortedGeometryCategory
PortedPoint = PortedPoint
PortedSegment = PortedSegment
PortedSiteEvent = PortedSiteEvent
PortedSourceCategory = PortedSourceCategory
PortedVertex = PortedVertex

BoundPortedBuildersPair = Tuple[BoundBuilder, PortedBuilder]
BoundPortedCellsPair = Tuple[BoundCell, PortedCell]
BoundPortedMaybeCellsPair = Tuple[Optional[BoundCell], Optional[PortedCell]]
BoundPortedCircleEventsPair = Tuple[BoundCircleEvent, PortedCircleEvent]
BoundPortedGeometryCategoriesPair = Tuple[BoundGeometryCategory,
                                          PortedGeometryCategory]
BoundPortedEdgesPair = Tuple[BoundEdge, PortedEdge]
BoundPortedMaybeEdgesPair = Tuple[Optional[BoundEdge], Optional[PortedEdge]]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]
BoundPortedSiteEventsPair = Tuple[BoundSiteEvent, PortedSiteEvent]
BoundPortedEventsPair = Union[BoundPortedCircleEventsPair,
                              BoundPortedSiteEventsPair]
BoundPortedSourceCategoriesPair = Tuple[BoundSourceCategory,
                                        PortedSourceCategory]
BoundPortedVerticesPair = Tuple[BoundVertex, PortedVertex]


def enum_to_values(cls: Type[Enum]) -> List[Enum]:
    return [value for _, value in sorted(cls.__members__.items())]


bound_geometry_categories = enum_to_values(BoundGeometryCategory)
bound_source_categories = enum_to_values(BoundSourceCategory)
ported_geometry_categories = enum_to_values(PortedGeometryCategory)
ported_source_categories = enum_to_values(PortedSourceCategory)

equivalence = is_


def transpose_pairs(pairs: List[Tuple[Domain, Range]]
                    ) -> Tuple[List[Domain], List[Range]]:
    return tuple(map(list, zip(*pairs))) if pairs else ([], [])


def to_maybe_equals(equals: Callable[[Domain, Range], bool]
                    ) -> Callable[[Optional[Domain], Optional[Range]], bool]:
    def maybe_equals(left: Optional[Domain], right: Optional[Range]) -> bool:
        return ((left is None) is (right is None)
                and (left is None or equals(left, right)))

    return maybe_equals


def are_bound_ported_builders_equal(bound: BoundBuilder,
                                    ported: PortedBuilder) -> bool:
    return (bound.index == ported.index
            and all(map(are_bound_ported_site_events_equal, bound.site_events,
                        ported.site_events))
            and bound.site_event_index == ported.site_event_index)


def are_bound_ported_cells_equal(bound: BoundCell, ported: PortedCell) -> bool:
    return (bound.source_index == ported.source_index
            and bound.source_category == ported.source_category)


are_bound_ported_maybe_cells_equal = to_maybe_equals(
        are_bound_ported_cells_equal)


def are_bound_ported_circle_events_equal(bound: BoundCircleEvent,
                                         ported: PortedCircleEvent) -> bool:
    return (bound.center_x == ported.center_x
            and bound.center_y == ported.center_y
            and bound.lower_x == ported.lower_x
            and bound.is_active is ported.is_active)


def are_bound_ported_edges_equal(bound: BoundEdge, ported: PortedEdge
                                 ) -> bool:
    return (are_bound_ported_maybe_vertices_equal(bound.start, ported.start)
            and are_bound_ported_maybe_edges_equal(bound.twin, ported.twin)
            and are_bound_ported_maybe_edges_equal(bound.prev, ported.prev)
            and are_bound_ported_maybe_edges_equal(bound.next, ported.next)
            and are_bound_ported_maybe_cells_equal(bound.cell, ported.cell)
            and bound.is_linear is ported.is_linear
            and bound.is_primary is ported.is_primary)


are_bound_ported_maybe_edges_equal = to_maybe_equals(
        are_bound_ported_edges_equal)


def are_bound_ported_points_equal(bound: BoundPoint, ported: PortedPoint
                                  ) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_segments_equal(bound: BoundSegment, ported: PortedSegment
                                    ) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end))


def are_bound_ported_site_events_equal(bound: BoundSiteEvent,
                                       ported: PortedSiteEvent) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end)
            and bound.sorted_index == ported.sorted_index
            and bound.initial_index == ported.initial_index
            and bound.is_inverse is ported.is_inverse
            and bound.source_category == ported.source_category)


def are_bound_ported_vertices_equal(bound: BoundVertex, ported: PortedVertex
                                    ) -> bool:
    return bound.x == ported.x and bound.y == ported.y


are_bound_ported_maybe_vertices_equal = to_maybe_equals(
        are_bound_ported_vertices_equal)


def to_bound_with_ported_builders_pair(index: int,
                                       site_events_pair
                                       : List[BoundPortedSiteEventsPair]
                                       ) -> BoundPortedBuildersPair:
    bound_site_events, ported_site_events = site_events_pair
    return (BoundBuilder(index, bound_site_events),
            PortedBuilder(index, ported_site_events))


def to_bound_with_ported_cells_pair(source_index: int,
                                    source_categories_pair
                                    : BoundPortedSourceCategoriesPair,
                                    incident_edges_pair
                                    : BoundPortedMaybeEdgesPair
                                    ) -> BoundPortedCellsPair:
    bound_source_category, ported_source_category = source_categories_pair
    bound_incident_edge, ported_incident_edge = incident_edges_pair
    return (BoundCell(source_index, bound_source_category,
                      bound_incident_edge),
            PortedCell(source_index, ported_source_category,
                       ported_incident_edge))


def to_bound_with_ported_circle_events_pair(center_x: int,
                                            center_y: int,
                                            lower_x: int,
                                            is_active: bool
                                            ) -> BoundPortedCircleEventsPair:
    return (BoundCircleEvent(center_x, center_y, lower_x, is_active),
            PortedCircleEvent(center_x, center_y, lower_x, is_active))


def to_bound_with_ported_edges_pair(starts_pair: BoundPortedVerticesPair,
                                    twins_pair: BoundPortedMaybeEdgesPair,
                                    prev_edges_pair: BoundPortedMaybeEdgesPair,
                                    next_edges_pair: BoundPortedMaybeEdgesPair,
                                    cells_pair: BoundPortedMaybeCellsPair,
                                    is_linear: bool,
                                    is_primary: bool) -> BoundPortedEdgesPair:
    bound_start, ported_start = starts_pair
    bound_twin, ported_twin = twins_pair
    bound_prev, ported_prev = prev_edges_pair
    bound_next, ported_next = next_edges_pair
    bound_cell, ported_cell = cells_pair
    return (BoundEdge(bound_start, bound_twin, bound_prev, bound_next,
                      bound_cell, is_linear, is_primary),
            PortedEdge(ported_start, ported_twin, ported_prev, ported_next,
                       ported_cell, is_linear, is_primary))


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_segments_pair(starts_pair: BoundPortedPointsPair,
                                       ends_pair: BoundPortedPointsPair
                                       ) -> BoundPortedSegmentsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    return (BoundSegment(bound_start, bound_end),
            PortedSegment(ported_start, ported_end))


def to_bound_with_ported_site_events_pair(starts_pair: BoundPortedPointsPair,
                                          ends_pair: BoundPortedPointsPair,
                                          sorted_index: int,
                                          initial_index: int,
                                          is_inverse: bool,
                                          source_categories
                                          : BoundPortedSourceCategoriesPair
                                          ) -> BoundPortedSiteEventsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    bound_source_category, ported_source_category = source_categories
    return (BoundSiteEvent(bound_start, bound_end, sorted_index, initial_index,
                           is_inverse, bound_source_category),
            PortedSiteEvent(ported_start, ported_end, sorted_index,
                            initial_index, is_inverse, ported_source_category))


def to_bound_with_ported_vertices_pair(x: int,
                                       y: int,
                                       incident_edges_pair
                                       : BoundPortedMaybeEdgesPair
                                       ) -> BoundPortedVerticesPair:
    bound_incident_edge, ported_incident_edge = incident_edges_pair
    return (BoundVertex(x, y, bound_incident_edge),
            PortedVertex(x, y, ported_incident_edge))


recursive = partial(strategies.recursive,
                    max_leaves=2)


def to_maybe_pairs(strategy: Strategy[Tuple[Domain, Range]]
                   ) -> Strategy[Tuple[Optional[Domain], Optional[Range]]]:
    return to_pairs(strategies.none()) | strategy


def to_pairs(strategy: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(strategy, strategy)
