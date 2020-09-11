from hypothesis import strategies

from tests.strategies import coordinates
from tests.utils import (to_bound_with_ported_points_pair,
                         to_bound_with_ported_segments_pair)

coordinates = coordinates
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
segments_pairs = strategies.builds(to_bound_with_ported_segments_pair,
                                   points_pairs, points_pairs)
