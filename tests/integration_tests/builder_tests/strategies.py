from typing import Tuple

from hypothesis import strategies
from hypothesis_geometry import planar
from hypothesis_geometry.hints import Contour as RawContour

from tests.strategies import (integers_32,
                              sizes)
from tests.utils import (BoundPoint,
                         BoundPortedBuildersPair,
                         BoundPortedBuildersWithDiagramsPair,
                         BoundPortedEdgesPair,
                         BoundPortedPointsListsPair,
                         BoundPortedPointsPair,
                         BoundPortedSegmentsListsPair,
                         BoundSegment,
                         PortedPoint,
                         PortedSegment,
                         Strategy,
                         bound_source_categories,
                         ported_source_categories,
                         recursive,
                         to_bound_with_ported_builders_pair,
                         to_bound_with_ported_cells_pair,
                         to_bound_with_ported_diagrams_pair,
                         to_bound_with_ported_edges_pair,
                         to_bound_with_ported_points_pair,
                         to_bound_with_ported_site_events_pair,
                         to_bound_with_ported_vertices_pair,
                         to_maybe_pairs,
                         to_pairs,
                         transpose_pairs)

booleans = strategies.booleans()
coordinates = integers_32
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)


def points_pair_to_coordinates(points_pair: BoundPortedPointsPair
                               ) -> Tuple[int, int]:
    bound, _ = points_pair
    return bound.x, bound.y


unique_points_lists_pairs = (
    (strategies.lists(points_pairs,
                      unique_by=points_pair_to_coordinates)
     .map(transpose_pairs)))


def raw_contour_to_segments_lists_pair(raw: RawContour
                                       ) -> BoundPortedSegmentsListsPair:
    raw_start = raw[-1]
    bound_start, ported_start = BoundPoint(*raw_start), PortedPoint(*raw_start)
    bound, ported = [], []
    for raw_end in raw:
        bound_end, ported_end = BoundPoint(*raw_end), PortedPoint(*raw_end)
        bound.append(BoundSegment(bound_start, bound_end))
        ported.append(PortedSegment(ported_start, ported_end))
        bound_start, ported_start = bound_end, ported_end
    return bound, ported


non_crossing_or_overlapping_segments_lists_pairs = (
    planar.contours(coordinates).map(raw_contour_to_segments_lists_pair))
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
site_events_pairs = strategies.builds(to_bound_with_ported_site_events_pair,
                                      points_pairs, points_pairs, sizes, sizes,
                                      booleans, source_categories_pairs)
site_events_lists_pairs = (strategies.lists(site_events_pairs)
                           .map(transpose_pairs))
empty_lists_pairs = to_pairs(strategies.builds(list))
empty_builders_pairs = strategies.builds(to_bound_with_ported_builders_pair,
                                         sizes, empty_lists_pairs)


def initialize_builders(builders: BoundPortedBuildersPair,
                        points_lists: BoundPortedPointsListsPair,
                        segments_lists: BoundPortedSegmentsListsPair
                        ) -> BoundPortedBuildersPair:
    bound, ported = builders
    for bound_point, ported_point in zip(*points_lists):
        bound.insert_point(bound_point.x, bound_point.y)
        ported.insert_point(ported_point.x, ported_point.y)
    for bound_segment, ported_segment in zip(*segments_lists):
        bound.insert_segment(bound_segment.start.x, bound_segment.start.y,
                             bound_segment.end.x, bound_segment.end.y)
        ported.insert_segment(ported_segment.start.x, ported_segment.start.y,
                              ported_segment.end.x, ported_segment.end.y)
    bound.init_sites_queue()
    ported.init_sites_queue()
    return builders


initialized_builders_pairs = (
        strategies.builds(initialize_builders,
                          empty_builders_pairs,
                          unique_points_lists_pairs,
                          empty_lists_pairs)
        | strategies.builds(initialize_builders,
                            empty_builders_pairs,
                            empty_lists_pairs,
                            non_crossing_or_overlapping_segments_lists_pairs))
builders_pairs = strategies.builds(to_bound_with_ported_builders_pair,
                                   sizes, site_events_lists_pairs)
nones_pairs = to_pairs(strategies.none())
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))


def to_edges_pairs(base: Strategy[BoundPortedEdgesPair]
                   ) -> Strategy[BoundPortedEdgesPair]:
    return strategies.builds(
            to_bound_with_ported_edges_pair,
            to_maybe_pairs(strategies.builds(
                    to_bound_with_ported_vertices_pair, coordinates,
                    coordinates, base)),
            base, base, base,
            to_maybe_pairs(strategies.builds(to_bound_with_ported_cells_pair,
                                             sizes, source_categories_pairs,
                                             base)),
            booleans, booleans)


edges_pairs = recursive(strategies.builds(to_bound_with_ported_edges_pair,
                                          nones_pairs, nones_pairs,
                                          nones_pairs, nones_pairs,
                                          nones_pairs, booleans, booleans),
                        to_edges_pairs)
maybe_edges_pairs = to_maybe_pairs(edges_pairs)
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair, sizes,
                                source_categories_pairs, maybe_edges_pairs)
vertices_pairs = strategies.builds(to_bound_with_ported_vertices_pair,
                                   coordinates, coordinates, maybe_edges_pairs)
cells_lists_pairs = strategies.lists(cells_pairs).map(transpose_pairs)
edges_lists_pairs = strategies.lists(edges_pairs).map(transpose_pairs)
vertices_lists_pairs = strategies.lists(vertices_pairs).map(transpose_pairs)
diagrams_pairs = strategies.builds(to_bound_with_ported_diagrams_pair,
                                   cells_lists_pairs, edges_lists_pairs,
                                   vertices_lists_pairs)


def initialize_diagrams(builders_with_diagrams_pair
                        : BoundPortedBuildersWithDiagramsPair
                        ) -> BoundPortedBuildersWithDiagramsPair:
    (bound_builder, bound_diagram), _ = builders_with_diagrams_pair
    bound_diagram._reserve(len(bound_builder.site_events))
    return builders_with_diagrams_pair


initialized_builders_with_diagrams_pairs = (
    (strategies.tuples(initialized_builders_pairs, diagrams_pairs)
     .map(transpose_pairs)
     .map(initialize_diagrams)))
