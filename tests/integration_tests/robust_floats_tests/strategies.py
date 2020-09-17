from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import to_bound_with_ported_robust_floats_pair

doubles = doubles
non_negative_doubles = doubles.map(abs)
non_zero_doubles = doubles.filter(bool)
robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, doubles, doubles)
non_zero_robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, non_zero_doubles, doubles)
non_negative_robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, non_negative_doubles, doubles)
