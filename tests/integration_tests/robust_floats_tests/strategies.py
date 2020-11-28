from hypothesis import strategies

from tests.integration_tests.utils import (
    to_bound_with_ported_robust_floats_pair)
from tests.strategies import doubles

doubles = doubles
robust_floats_pairs = strategies.builds(
        to_bound_with_ported_robust_floats_pair, doubles, doubles)
