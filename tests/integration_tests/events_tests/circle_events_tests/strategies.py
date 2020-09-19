from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import to_bound_with_ported_circle_events_pair

booleans = strategies.booleans()
doubles = doubles
circle_events_pairs = strategies.builds(
        to_bound_with_ported_circle_events_pair, doubles, doubles, doubles,
        booleans)
