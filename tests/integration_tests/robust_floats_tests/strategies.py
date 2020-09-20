from hypothesis import strategies

from tests.strategies import doubles
from tests.utils import to_bound_with_ported_robust_floats_pair

doubles = doubles
robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, doubles, doubles)
