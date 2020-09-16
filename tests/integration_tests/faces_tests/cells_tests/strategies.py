from hypothesis import strategies

from tests.strategies import (doubles,
                              sizes)
from tests.utils import (BoundPortedEdgesPair,
                         Strategy,
                         bound_source_categories,
                         ported_source_categories,
                         to_bound_with_ported_cells_pair,
                         to_bound_with_ported_edges_pair,
                         to_bound_with_ported_vertices_pair,
                         to_maybe_pairs,
                         to_pairs)

booleans = strategies.booleans()
coordinates = doubles
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


edges_pairs = strategies.recursive(
        strategies.builds(to_bound_with_ported_edges_pair, nones_pairs,
                          nones_pairs, nones_pairs, nones_pairs, nones_pairs,
                          booleans, booleans),
        to_edges_pairs)
maybe_edges_pairs = to_maybe_pairs(edges_pairs)
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair, sizes,
                                source_categories_pairs, maybe_edges_pairs)
