from hypothesis import strategies

from tests.bind_tests.utils import bound_source_categories
from tests.integration_tests.utils import (to_bound_with_ported_cells_pair,
                                           to_bound_with_ported_edges_pair,
                                           to_bound_with_ported_vertices_pair)
from tests.port_tests.utils import ported_source_categories
from tests.strategies import (doubles,
                              sizes)
from tests.utils import to_maybe_pairs

booleans = strategies.booleans()
coordinates = doubles
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair, sizes,
                                source_categories_pairs)
vertices_pairs = strategies.builds(to_bound_with_ported_vertices_pair,
                                   coordinates, coordinates)
maybe_vertices_pairs = to_maybe_pairs(vertices_pairs)
edges_pairs = strategies.builds(to_bound_with_ported_edges_pair,
                                maybe_vertices_pairs, cells_pairs, booleans,
                                booleans)
