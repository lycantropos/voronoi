from hypothesis import strategies

from tests.strategies import (integers_32,
                              sizes)
from tests.utils import (bound_source_categories,
                         ported_source_categories,
                         to_bound_with_ported_builders_pair,
                         to_bound_with_ported_points_pair,
                         to_bound_with_ported_site_events_pair,
                         transpose_pairs)

booleans = strategies.booleans()
coordinates = integers_32
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 coordinates, coordinates)
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
site_events_pairs = strategies.builds(to_bound_with_ported_site_events_pair,
                                      points_pairs, points_pairs, sizes, sizes,
                                      booleans, source_categories_pairs)
site_events_lists_pairs = (strategies.lists(site_events_pairs)
                           .map(transpose_pairs))
builders_pairs = strategies.builds(to_bound_with_ported_builders_pair,
                                   sizes, site_events_lists_pairs)
