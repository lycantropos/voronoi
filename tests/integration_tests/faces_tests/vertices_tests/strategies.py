from hypothesis import strategies

from tests.integration_tests.utils import to_bound_with_ported_vertices_pair
from tests.strategies import doubles

coordinates = doubles
vertices_pairs = strategies.builds(to_bound_with_ported_vertices_pair,
                                   coordinates, coordinates)
