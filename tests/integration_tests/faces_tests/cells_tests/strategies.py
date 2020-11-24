from hypothesis import strategies

from tests.strategies import (doubles,
                              sizes)
from tests.utils import (bound_source_categories,
                         ported_source_categories,
                         to_bound_with_ported_cells_pair,
                         to_pairs)

booleans = strategies.booleans()
coordinates = doubles
nones_pairs = to_pairs(strategies.none())
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair, sizes,
                                source_categories_pairs)
