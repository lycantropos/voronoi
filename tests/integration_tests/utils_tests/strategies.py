from hypothesis import strategies

from tests.strategies import (doubles,
                              integers_32,
                              sizes)
from tests.utils import to_bound_with_ported_points_pair

coordinates = integers_32
sizes = sizes
floats = doubles
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
