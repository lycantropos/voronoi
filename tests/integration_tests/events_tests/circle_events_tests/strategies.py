from hypothesis import strategies

from tests.strategies import (doubles,
                              integers_32,
                              sizes)
from tests.utils import (bound_source_categories,
                         ported_source_categories,
                         to_bound_with_ported_circle_events_pair,
                         to_bound_with_ported_points_pair,
                         to_bound_with_ported_site_events_pair)

booleans = strategies.booleans()
coordinates = integers_32
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
circle_events_pairs = strategies.builds(
        to_bound_with_ported_circle_events_pair, doubles, doubles, doubles,
        booleans)
site_events_pairs = strategies.builds(to_bound_with_ported_site_events_pair,
                                      points_pairs, points_pairs, sizes, sizes,
                                      booleans, source_categories_pairs)
