from typing import Tuple

from hypothesis import strategies
from hypothesis_geometry import planar

from tests.bind_tests.hints import (BoundPoint,
                                    BoundSegment)
from tests.bind_tests.utils import bound_source_categories
from tests.integration_tests.hints import (BoundPortedBuildersPair,
                                           BoundPortedBuildersWithDiagramsPair,
                                           BoundPortedPointsListsPair,
                                           BoundPortedPointsPair,
                                           BoundPortedSegmentsListsPair,
                                           BoundPortedSegmentsPair,
                                           BoundPortedSiteEventsListsPair)
from tests.integration_tests.utils import (
    to_bound_ported_multipoints_pair,
    to_bound_ported_multisegments_pair,
    to_bound_with_ported_builders_pair,
    to_bound_with_ported_cells_pair,
    to_bound_with_ported_diagrams_pair,
    to_bound_with_ported_edges_pair,
    to_bound_with_ported_points_pair,
    to_bound_with_ported_site_events_pair,
    to_bound_with_ported_vertices_pair)
from tests.port_tests.hints import (PortedPoint,
                                    PortedSegment)
from tests.port_tests.utils import ported_source_categories
from tests.strategies import (integers_32,
                              sizes)
from tests.utils import (RawSegment,
                         to_maybe_pairs,
                         to_pairs,
                         transpose_pairs)

booleans = strategies.booleans()
coordinates = integers_32
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)


def raw_segment_to_segments_pair(raw: RawSegment) -> BoundPortedSegmentsPair:
    return (BoundSegment(BoundPoint(raw.start.x, raw.start.y),
                         BoundPoint(raw.end.x, raw.end.y)),
            PortedSegment(PortedPoint(raw.start.x, raw.start.y),
                          PortedPoint(raw.end.x, raw.end.y)))


segments_pairs = planar.segments(coordinates).map(raw_segment_to_segments_pair)


def points_pair_to_coordinates(points_pair: BoundPortedPointsPair
                               ) -> Tuple[int, int]:
    bound, _ = points_pair
    return bound.x, bound.y


multipoints_pairs = planar.multipoints(coordinates).map(
        to_bound_ported_multipoints_pair)
multisegments_pairs = (planar.multisegments(coordinates)
                       .map(to_bound_ported_multisegments_pair))
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
site_events_pairs = strategies.builds(to_bound_with_ported_site_events_pair,
                                      points_pairs, points_pairs, sizes, sizes,
                                      booleans, source_categories_pairs)
non_empty_site_events_lists_pairs = (strategies.lists(site_events_pairs,
                                                      min_size=1)
                                     .map(transpose_pairs))


def to_indices_with_site_events_lists_pairs(
        site_events_pair: BoundPortedSiteEventsListsPair
) -> Tuple[int, BoundPortedSiteEventsListsPair]:
    bound_events, ported_events = site_events_pair
    return strategies.tuples(strategies.integers(0, len(bound_events)),
                             strategies.just(site_events_pair))


indices_with_non_empty_site_events_lists_pairs = (
    (non_empty_site_events_lists_pairs
     .flatmap(to_indices_with_site_events_lists_pairs)))
empty_lists_pairs = to_pairs(strategies.builds(list))
empty_builders_pairs = strategies.builds(to_bound_with_ported_builders_pair,
                                         sizes, empty_lists_pairs)


def to_valid_multipoints_builders_pair(builders: BoundPortedBuildersPair,
                                       multipoints: BoundPortedPointsListsPair
                                       ) -> BoundPortedBuildersPair:
    bound, ported = builders
    for bound_point, ported_point in zip(*multipoints):
        bound.insert_point(bound_point)
        ported.insert_point(ported_point)
    return bound, ported


def to_valid_multisegments_builders_pair(builders: BoundPortedBuildersPair,
                                         multisegments
                                         : BoundPortedSegmentsListsPair
                                         ) -> BoundPortedBuildersPair:
    bound, ported = builders
    for bound_segment, ported_segment in zip(*multisegments):
        bound.insert_segment(bound_segment)
        ported.insert_segment(ported_segment)
    return bound, ported


valid_builders_pairs = (
        strategies.builds(to_valid_multipoints_builders_pair,
                          empty_builders_pairs, multipoints_pairs)
        | strategies.builds(to_valid_multisegments_builders_pair,
                            empty_builders_pairs, multisegments_pairs))
builders_pairs = (strategies.builds(to_bound_with_ported_builders_pair, sizes,
                                    non_empty_site_events_lists_pairs)
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
empty_diagrams_pairs = strategies.builds(to_bound_with_ported_diagrams_pair,
                                         empty_lists_pairs, empty_lists_pairs,
                                         empty_lists_pairs)
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair, sizes,
                                source_categories_pairs)
vertices_pairs = strategies.builds(to_bound_with_ported_vertices_pair,
                                   coordinates, coordinates)
edges_pairs = strategies.builds(to_bound_with_ported_edges_pair,
                                to_maybe_pairs(vertices_pairs), cells_pairs,
                                booleans, booleans)
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


initialized_valid_builders_with_diagrams_pairs = (
    (strategies.tuples(initialized_valid_builders_pairs, diagrams_pairs)
     .map(transpose_pairs)
     .map(initialize_diagrams)))
