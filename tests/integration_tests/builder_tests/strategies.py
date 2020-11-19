from operator import itemgetter
from typing import Tuple

from hypothesis import strategies
from hypothesis_geometry import planar
from hypothesis_geometry.hints import Segment as RawSegment

from tests.strategies import (integers_32,
                              sizes)
from tests.utils import (BoundPoint,
                         BoundPortedBuildersPair,
                         BoundPortedBuildersWithDiagramsPair,
                         BoundPortedEdgesPair,
                         BoundPortedPointsListsPair,
                         BoundPortedPointsPair,
                         BoundPortedSegmentsListsPair,
                         BoundPortedSegmentsPair,
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
                         to_multipoints_with_multisegments_pairs,
                         to_pairs,
                         transpose_pairs)

booleans = strategies.booleans()
coordinates = integers_32
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)


def raw_segment_to_segments_pair(raw: RawSegment) -> BoundPortedSegmentsPair:
    (start_x, start_y), (end_x, end_y) = raw
    return (BoundSegment(BoundPoint(start_x, start_y),
                         BoundPoint(end_x, end_y)),
            PortedSegment(PortedPoint(start_x, start_y),
                          PortedPoint(end_x, end_y)))


segments_pairs = planar.segments(coordinates).map(raw_segment_to_segments_pair)


def points_pair_to_coordinates(points_pair: BoundPortedPointsPair
                               ) -> Tuple[int, int]:
    bound, _ = points_pair
    return bound.x, bound.y


multipoints_with_multisegments_pairs = (
    (planar.mixes(coordinates,
                  max_multipolygon_size=0)
     .map(itemgetter(0, 1))
     .map(to_multipoints_with_multisegments_pairs)))
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


def to_valid_builders_pair(builders: BoundPortedBuildersPair,
                           multipoints_with_multisegments
                           : Tuple[BoundPortedPointsListsPair,
                                   BoundPortedSegmentsListsPair]
                           ) -> BoundPortedBuildersPair:
    multipoints, multisegments = multipoints_with_multisegments
    bound, ported = builders
    for bound_point, ported_point in zip(*multipoints):
        bound.insert_point(bound_point)
        ported.insert_point(ported_point)
    for bound_segment, ported_segment in zip(*multisegments):
        bound.insert_segment(bound_segment)
        ported.insert_segment(ported_segment)
    return builders


valid_builders_pairs = strategies.builds(
        to_valid_builders_pair, empty_builders_pairs,
        multipoints_with_multisegments_pairs)
builders_pairs = (strategies.builds(to_bound_with_ported_builders_pair, sizes,
                                    site_events_lists_pairs)
                  | valid_builders_pairs)


def init_sites_queue(builders: BoundPortedBuildersPair
                     ) -> BoundPortedBuildersPair:
    bound, ported = builders
    bound.init_sites_queue()
    ported.init_sites_queue()
    return builders


initialized_builders_pairs = builders_pairs.map(init_sites_queue)
initialized_valid_builders_pairs = valid_builders_pairs.map(init_sites_queue)
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


empty_diagrams_pairs = strategies.builds(to_bound_with_ported_diagrams_pair,
                                         empty_lists_pairs, empty_lists_pairs,
                                         empty_lists_pairs)
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
    ((bound_builder, bound_diagram),
     (ported_builder, ported_diagram)) = builders_with_diagrams_pair
    bound_diagram._reserve(len(bound_builder.site_events))
    ported_diagram._reserve(len(ported_builder.site_events))
    return builders_with_diagrams_pair


initialized_valid_builders_with_diagrams_pairs = (
    (strategies.tuples(initialized_valid_builders_pairs, diagrams_pairs)
     .map(transpose_pairs)
     .map(initialize_diagrams)))
