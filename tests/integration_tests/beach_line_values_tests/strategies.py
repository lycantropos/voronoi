from hypothesis import strategies

from tests.bind_tests.utils import bound_source_categories
from tests.integration_tests.utils import (
    to_bound_with_ported_cells_pair,
    to_bound_with_ported_circle_events_pair,
    to_bound_with_ported_edges_pair,
    to_bound_with_ported_vertices_pair)
from tests.port_tests.utils import ported_source_categories
from tests.strategies import (doubles,
                              sizes)
from tests.utils import (to_maybe_pairs,
                         to_pairs)

booleans = strategies.booleans()
nones_pairs = to_pairs(strategies.none())
coordinates = doubles
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
edges_pairs = strategies.builds(
        to_bound_with_ported_edges_pair,
        to_maybe_pairs(strategies.builds(to_bound_with_ported_vertices_pair,
                                         coordinates, coordinates)),
        strategies.builds(to_bound_with_ported_cells_pair, sizes,
                          source_categories_pairs),
        booleans, booleans)
maybe_edges_pairs = to_maybe_pairs(edges_pairs)
circle_events_pairs = strategies.builds(
        to_bound_with_ported_circle_events_pair, doubles, doubles, doubles,
        booleans)
maybe_circle_events_pairs = to_maybe_pairs(circle_events_pairs)
