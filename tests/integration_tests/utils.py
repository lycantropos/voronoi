from math import isnan
from typing import List

from tests.bind_tests.hints import (BoundBeachLineKey,
                                    BoundBeachLineValue,
                                    BoundBigFloat,
                                    BoundBigInt,
                                    BoundBuilder,
                                    BoundCell,
                                    BoundCircleEvent,
                                    BoundDiagram,
                                    BoundEdge,
                                    BoundPoint,
                                    BoundRobustDifference,
                                    BoundRobustFloat,
                                    BoundSegment,
                                    BoundSiteEvent,
                                    BoundVertex)
from tests.bind_tests.utils import (to_bound_multipoint,
                                    to_bound_multisegment)
from tests.integration_tests.hints import (BoundPortedBeachLineKeysPair,
                                           BoundPortedBigFloatsPair,
                                           BoundPortedBigIntsPair,
                                           BoundPortedBuildersPair,
                                           BoundPortedCellsListsPair,
                                           BoundPortedCellsPair,
                                           BoundPortedCircleEventsPair,
                                           BoundPortedDiagramsPair,
                                           BoundPortedEdgesListsPair,
                                           BoundPortedEdgesPair,
                                           BoundPortedMaybeVerticesPair,
                                           BoundPortedPointsListsPair,
                                           BoundPortedPointsPair,
                                           BoundPortedRobustDifferencesPair,
                                           BoundPortedRobustFloatsPair,
                                           BoundPortedSegmentsListsPair,
                                           BoundPortedSegmentsPair,
                                           BoundPortedSiteEventsPair,
                                           BoundPortedSourceCategoriesPair,
                                           BoundPortedVerticesListsPair,
                                           BoundPortedVerticesPair)
from tests.port_tests.hints import (PortedBeachLineKey,
                                    PortedBeachLineValue,
                                    PortedBigFloat,
                                    PortedBigInt,
                                    PortedBuilder,
                                    PortedCell,
                                    PortedCircleEvent,
                                    PortedDiagram,
                                    PortedEdge,
                                    PortedPoint,
                                    PortedRobustDifference,
                                    PortedRobustFloat,
                                    PortedSegment,
                                    PortedSiteEvent,
                                    PortedVertex)
from tests.port_tests.utils import (to_ported_multipoint,
                                    to_ported_multisegment)
from tests.utils import (RawMultipoint,
                         RawMultisegment,
                         to_maybe_equals,
                         to_sequences_equals)
from voronoi.enums import ComparisonResult
from voronoi.events.models import ULPS
from voronoi.utils import compare_floats


def are_bound_ported_beach_line_keys_equal(bound: BoundBeachLineKey,
                                           ported: PortedBeachLineKey) -> bool:
    return (are_bound_ported_site_events_equal(bound.left_site,
                                               ported.left_site)
            and are_bound_ported_site_events_equal(bound.right_site,
                                                   ported.right_site))


def are_bound_ported_beach_line_values_equal(bound: BoundBeachLineValue,
                                             ported: PortedBeachLineValue
                                             ) -> bool:
    return (are_bound_ported_maybe_edges_equal(bound.edge, ported.edge)
            and are_bound_ported_maybe_circle_events_equal(
                    bound.circle_event, ported.circle_event))


def are_bound_ported_big_floats_equal(bound: BoundBigFloat,
                                      ported: PortedBigFloat) -> bool:
    return (bound.mantissa == ported.mantissa
            and bound.exponent == ported.exponent
            # we are not comparing exponents in this case
            # because ``sqrt`` of negative number returns ``-nan(ind)``on MSVC
            # and ``nan`` on other compilers
            or isnan(bound.mantissa) and isnan(ported.mantissa))


def are_bound_ported_big_ints_equal(bound: BoundBigInt,
                                    ported: PortedBigInt) -> bool:
    return bound.digits == ported.digits and bound.sign == ported.sign


def are_bound_ported_builders_equal(bound: BoundBuilder,
                                    ported: PortedBuilder) -> bool:
    return (bound.index == ported.index
            and are_bound_ported_site_events_lists_equal(bound.site_events,
                                                         ported.site_events)
            and bound.site_event_index == ported.site_event_index)


def are_bound_ported_cells_equal(bound: BoundCell, ported: PortedCell) -> bool:
    return (bound.source_index == ported.source_index
            and bound.source_category == ported.source_category)


are_bound_ported_cells_lists_equal = to_sequences_equals(
        are_bound_ported_cells_equal)
are_bound_ported_maybe_cells_equal = to_maybe_equals(
        are_bound_ported_cells_equal)


def are_bound_ported_circle_events_equal(bound: BoundCircleEvent,
                                         ported: PortedCircleEvent) -> bool:
    return (are_floats_equivalent(bound.center_x, ported.center_x)
            and are_floats_equivalent(bound.center_y, ported.center_y)
            and are_floats_equivalent(bound.lower_x, ported.lower_x)
            and bound.is_active is ported.is_active)


are_bound_ported_maybe_circle_events_equal = to_maybe_equals(
        are_bound_ported_circle_events_equal)


def are_bound_ported_diagrams_equal(bound: BoundDiagram, ported: PortedDiagram
                                    ) -> bool:
    return (are_bound_ported_cells_lists_equal(bound.cells, ported.cells)
            and are_bound_ported_edges_lists_equal(bound.edges, ported.edges)
            and are_bound_ported_vertices_lists_equal(bound.vertices,
                                                      ported.vertices))


def are_bound_ported_edges_equal(bound: BoundEdge, ported: PortedEdge
                                 ) -> bool:
    return (are_bound_ported_maybe_vertices_equal(bound.start, ported.start)
            and bound.is_linear is ported.is_linear
            and bound.is_primary is ported.is_primary)


are_bound_ported_edges_lists_equal = to_sequences_equals(
        are_bound_ported_edges_equal)
are_bound_ported_maybe_edges_equal = to_maybe_equals(
        are_bound_ported_edges_equal)


def are_bound_ported_points_equal(bound: BoundPoint, ported: PortedPoint
                                  ) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_robust_differences_equal(bound: BoundRobustDifference,
                                              ported: PortedRobustDifference
                                              ) -> bool:
    return (are_bound_ported_robust_floats_equal(bound.minuend, ported.minuend)
            and are_bound_ported_robust_floats_equal(bound.subtrahend,
                                                     ported.subtrahend))


def are_bound_ported_robust_floats_equal(bound: BoundRobustFloat,
                                         ported: PortedRobustFloat) -> bool:
    return (are_floats_equivalent(bound.value, ported.value)
            and are_floats_equivalent(bound.relative_error,
                                      ported.relative_error))


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


are_bound_ported_site_events_lists_equal = to_sequences_equals(
        are_bound_ported_site_events_equal)


def are_bound_ported_vertices_equal(bound: BoundVertex, ported: PortedVertex
                                    ) -> bool:
    return (compare_floats(bound.x, ported.x, ULPS)
            is compare_floats(bound.y, ported.y, ULPS)
            is ComparisonResult.EQUAL)


are_bound_ported_vertices_lists_equal = to_sequences_equals(
        are_bound_ported_vertices_equal)
are_bound_ported_maybe_vertices_equal = to_maybe_equals(
        are_bound_ported_vertices_equal)


def are_floats_equivalent(left: float, right: float) -> bool:
    left_is_nan = isnan(left)
    return (left_is_nan is isnan(right)
            and (left_is_nan
                 or (compare_floats(left, right, ULPS)
                     is ComparisonResult.EQUAL)))


def to_bound_with_ported_beach_line_keys_pair(
        left_sites_pair: BoundPortedSiteEventsPair,
        right_sites_pair: BoundPortedSiteEventsPair
) -> BoundPortedBeachLineKeysPair:
    bound_left_site, ported_left_site = left_sites_pair
    bound_right_site, ported_right_site = right_sites_pair
    return (BoundBeachLineKey(bound_left_site, bound_right_site),
            PortedBeachLineKey(ported_left_site, ported_right_site))


def to_bound_with_ported_big_floats_pair(mantissa: float,
                                         exponent: int
                                         ) -> BoundPortedBigFloatsPair:
    return (BoundBigFloat(mantissa, exponent),
            PortedBigFloat(mantissa, exponent))


def to_bound_with_ported_big_ints_pair(sign: int, digits: List[int]
                                       ) -> BoundPortedBigIntsPair:
    return BoundBigInt(sign, digits), PortedBigInt(sign, digits)


def to_bound_with_ported_builders_pair(index: int,
                                       site_events_pair
                                       : List[BoundPortedSiteEventsPair]
                                       ) -> BoundPortedBuildersPair:
    bound_site_events, ported_site_events = site_events_pair
    return (BoundBuilder(index, bound_site_events),
            PortedBuilder(index, ported_site_events))


def to_bound_with_ported_cells_pair(source_index: int,
                                    source_categories_pair
                                    : BoundPortedSourceCategoriesPair
                                    ) -> BoundPortedCellsPair:
    bound_source_category, ported_source_category = source_categories_pair
    return (BoundCell(source_index, bound_source_category),
            PortedCell(source_index, ported_source_category))


def to_bound_with_ported_circle_events_pair(center_x: float,
                                            center_y: float,
                                            lower_x: float,
                                            is_active: bool
                                            ) -> BoundPortedCircleEventsPair:
    return (BoundCircleEvent(center_x, center_y, lower_x, is_active),
            PortedCircleEvent(center_x, center_y, lower_x, is_active))


def to_bound_with_ported_diagrams_pair(cells_pair: BoundPortedCellsListsPair,
                                       edges_pair: BoundPortedEdgesListsPair,
                                       vertices_pair
                                       : BoundPortedVerticesListsPair
                                       ) -> BoundPortedDiagramsPair:
    bound_cells, ported_cells = cells_pair
    bound_edges, ported_edges = edges_pair
    bound_vertices, ported_vertices = vertices_pair
    return (BoundDiagram(bound_cells, bound_edges, bound_vertices),
            PortedDiagram(ported_cells, ported_edges, ported_vertices))


def to_bound_with_ported_edges_pair(starts_pair: BoundPortedMaybeVerticesPair,
                                    cells_pair: BoundPortedCellsPair,
                                    is_linear: bool,
                                    is_primary: bool) -> BoundPortedEdgesPair:
    bound_start, ported_start = starts_pair
    bound_cell, ported_cell = cells_pair
    return (BoundEdge(bound_start, bound_cell, is_linear, is_primary),
            PortedEdge(ported_start, ported_cell, is_linear, is_primary))


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_robust_differences_pair(
        minuends_pair: BoundPortedRobustFloatsPair,
        subtrahends_pair: BoundPortedRobustFloatsPair
) -> BoundPortedRobustDifferencesPair:
    bound_minuend, ported_minuend = minuends_pair
    bound_subtrahend, ported_subtrahend = subtrahends_pair
    return (BoundRobustDifference(bound_minuend, bound_subtrahend),
            PortedRobustDifference(ported_minuend, ported_subtrahend))


def to_bound_with_ported_robust_floats_pair(value: float,
                                            relative_error: float
                                            ) -> BoundPortedRobustFloatsPair:
    return (BoundRobustFloat(value, relative_error),
            PortedRobustFloat(value, relative_error))


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


def to_bound_with_ported_vertices_pair(x: int, y: int
                                       ) -> BoundPortedVerticesPair:
    return BoundVertex(x, y), PortedVertex(x, y)


def to_bound_ported_multipoints_pair(raw_multipoint: RawMultipoint
                                     ) -> BoundPortedPointsListsPair:
    return (to_bound_multipoint(raw_multipoint),
            to_ported_multipoint(raw_multipoint))


def to_bound_ported_multisegments_pair(raw_multisegment: RawMultisegment
                                       ) -> BoundPortedSegmentsListsPair:
    return (to_bound_multisegment(raw_multisegment),
            to_ported_multisegment(raw_multisegment))
