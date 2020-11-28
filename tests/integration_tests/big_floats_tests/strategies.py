from hypothesis import strategies

from tests.integration_tests.utils import to_bound_with_ported_big_floats_pair
from tests.strategies import (doubles,
                              integers_32)

doubles = doubles
integers_32 = integers_32
big_floats_pairs = strategies.builds(to_bound_with_ported_big_floats_pair,
                                     doubles, integers_32)
non_zero_big_floats_pairs = strategies.builds(
        to_bound_with_ported_big_floats_pair, doubles.filter(bool),
        integers_32)
