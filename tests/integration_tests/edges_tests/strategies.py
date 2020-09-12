from hypothesis import strategies

from tests.strategies import integers_64
from tests.utils import to_bound_with_ported_edges_pair

booleans = strategies.booleans()
edges_pairs = strategies.builds(to_bound_with_ported_edges_pair,
                                integers_64, integers_64, booleans, booleans,
                                integers_64, integers_64)
