from hypothesis import strategies
from hypothesis_geometry import planar

from tests.strategies import (doubles,
                              integers_32,
                              sizes)
from tests.utils import (BoundPortedEdgesPair,
                         Strategy,
                         bound_source_categories,
                         ported_source_categories,
                         recursive,
                         to_bound_with_ported_cells_pair,
                         to_bound_with_ported_diagrams_pair,
                         to_bound_with_ported_edges_pair,
                         to_bound_with_ported_points_pair,
                         to_bound_with_ported_site_events_pair,
                         to_bound_with_ported_vertices_pair,
                         to_maybe_pairs,
                         to_multipoints_pair,
                         to_multisegments_pair,
                         to_pairs,
                         transpose_pairs)

booleans = strategies.booleans()
coordinates = doubles
nones_pairs = to_pairs(strategies.none())
empty_lists_pairs = to_pairs(strategies.builds(list))
empty_diagrams_pairs = strategies.builds(to_bound_with_ported_diagrams_pair,
                                         empty_lists_pairs, empty_lists_pairs,
                                         empty_lists_pairs)
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
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 integers_32, integers_32)
site_events_pairs = strategies.builds(to_bound_with_ported_site_events_pair,
                                      points_pairs, points_pairs, sizes, sizes,
                                      booleans, source_categories_pairs)
multipoints = planar.multipoints(integers_32).map(to_multipoints_pair)
multisegments = planar.multisegments(integers_32).map(to_multisegments_pair)
