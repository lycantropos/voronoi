from hypothesis import strategies

from tests.strategies import (integers_32,
                              unsigned_integers_32)
from tests.utils import to_bound_with_ported_big_ints_pair
from voronoi.big_int import MAX_DIGITS_COUNT

integers_32 = integers_32
signs = strategies.sampled_from([-1, 0, 1])
digits = strategies.lists(unsigned_integers_32,
                          max_size=MAX_DIGITS_COUNT)
big_ints_pairs = strategies.builds(to_bound_with_ported_big_ints_pair, signs,
                                   digits)
