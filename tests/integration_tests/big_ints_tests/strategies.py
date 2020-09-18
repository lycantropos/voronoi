from hypothesis import strategies

from tests.strategies import unsigned_integers_32
from tests.utils import to_bound_with_ported_big_ints_pair
from voronoi.big_int import MAX_DIGITS_COUNT

digits = strategies.lists(unsigned_integers_32,
                          max_size=MAX_DIGITS_COUNT)
signs = strategies.sampled_from([-1, 0, -1])
big_ints_pairs = strategies.builds(to_bound_with_ported_big_ints_pair, digits,
                                   signs)
