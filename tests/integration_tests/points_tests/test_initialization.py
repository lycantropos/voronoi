from hypothesis import given

from tests.utils import (BoundPoint,
                         PortedPoint,
                         are_bound_ported_points_equal)
from . import strategies


@given(strategies.integers_32, strategies.integers_32)
def test_basic(x: int, y: int) -> None:
    bound, ported = BoundPoint(x, y), PortedPoint(x, y)

    assert are_bound_ported_points_equal(bound, ported)
