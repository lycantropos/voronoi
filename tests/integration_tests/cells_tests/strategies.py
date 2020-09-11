from hypothesis import strategies

from tests.strategies import (integers_32,
                              integers_64,
                              sizes)
from tests.utils import to_bound_with_ported_cells_pair

booleans = strategies.booleans()
integers_64_lists = strategies.lists(integers_64)
cells_pairs = strategies.builds(to_bound_with_ported_cells_pair,
                                sizes, sizes, booleans, booleans, booleans,
                                booleans, integers_64_lists, integers_64_lists,
                                integers_32)
