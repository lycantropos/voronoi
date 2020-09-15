from hypothesis import strategies

from tests.strategies import (integers_32,
                              sizes)
from tests.utils import to_bound_with_ported_points_pair

coordinates = integers_32
sizes = sizes
floats = strategies.floats(allow_nan=False,
                           allow_infinity=False)
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
