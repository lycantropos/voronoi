from hypothesis import strategies

from tests.bind_tests.utils import bound_source_categories
from tests.integration_tests.utils import to_bound_with_ported_cells_pair
from tests.port_tests.utils import ported_source_categories
from tests.strategies import sizes

source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair, sizes,
                                source_categories_pairs)
