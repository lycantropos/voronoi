from hypothesis import strategies

from tests.integration_tests.utils import to_bound_with_ported_points_pair
from tests.strategies import (doubles,
                              integers_32,
                              integers_64,
                              sizes)

coordinates = integers_32
integers_64 = integers_64
sizes = sizes
floats = doubles
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
