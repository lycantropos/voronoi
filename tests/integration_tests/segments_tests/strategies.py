from hypothesis import strategies

from tests.integration_tests.utils import (to_bound_with_ported_points_pair,
                                           to_bound_with_ported_segments_pair)
from tests.strategies import integers_32

coordinates = integers_32
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
segments_pairs = strategies.builds(to_bound_with_ported_segments_pair,
                                   points_pairs, points_pairs)
