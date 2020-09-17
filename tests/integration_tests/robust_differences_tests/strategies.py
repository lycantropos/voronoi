from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import (to_bound_with_ported_robust_differences_pair,
                         to_bound_with_ported_robust_floats_pair)

doubles = doubles
non_zero_doubles = doubles.filter(bool)
robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, doubles, doubles)
non_zero_robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, non_zero_doubles, doubles)
robust_differences_pairs = strategies.builds(
        to_bound_with_ported_robust_differences_pair, robust_floats_pairs,
        robust_floats_pairs)
