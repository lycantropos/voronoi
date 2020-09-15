from hypothesis import strategies

from tests.strategies import integers_32
from tests.utils import to_bound_with_ported_circle_events_pair

booleans = strategies.booleans()
coordinates = integers_32
circle_events_pairs = strategies.builds(
        to_bound_with_ported_circle_events_pair, coordinates, coordinates,
        coordinates, booleans)
