from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import (to_bound_with_ported_vertices_pair,
                         to_pairs)

coordinates = doubles
maybe_edges_pairs = to_pairs(strategies.none())
vertices_pairs = strategies.builds(to_bound_with_ported_vertices_pair,
                                   coordinates, coordinates, maybe_edges_pairs)
