from hypothesis import strategies

from tests.strategies import (doubles,
                              integers_32)
from tests.utils import to_bound_with_ported_big_floats_pair

doubles = doubles
integers_32 = integers_32
big_floats_pairs = strategies.builds(to_bound_with_ported_big_floats_pair,
                                     doubles, integers_32)
non_negative_big_floats_pairs = strategies.builds(
        to_bound_with_ported_big_floats_pair, doubles.map(abs), integers_32)
non_zero_big_floats_pairs = strategies.builds(
        to_bound_with_ported_big_floats_pair, doubles.filter(bool),
        integers_32)
