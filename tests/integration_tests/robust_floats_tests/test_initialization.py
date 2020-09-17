from hypothesis import given

from tests.utils import (BoundRobustFloat,
                         PortedRobustFloat,
                         are_bound_ported_robust_floats_equal)
from . import strategies


@given(strategies.doubles, strategies.doubles)
def test_basic(value: int, relative_error: int) -> None:
    bound, ported = (BoundRobustFloat(value, relative_error),
                     PortedRobustFloat(value, relative_error))

    assert are_bound_ported_robust_floats_equal(bound, ported)
