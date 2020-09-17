from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import to_bound_with_ported_robust_floats_pair

doubles = doubles
non_negative_doubles = doubles.map(abs)
robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, doubles, doubles)
non_negative_robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, non_negative_doubles, doubles)
