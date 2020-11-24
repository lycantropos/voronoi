from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import to_bound_with_ported_vertices_pair

coordinates = doubles
vertices_pairs = strategies.builds(to_bound_with_ported_vertices_pair,
                                   coordinates, coordinates)
