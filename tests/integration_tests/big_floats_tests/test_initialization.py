from hypothesis import given

from tests.bind_tests.hints import BoundBigFloat
from tests.integration_tests.utils import are_bound_ported_big_floats_equal
from tests.port_tests.hints import PortedBigFloat
from . import strategies


@given(strategies.doubles, strategies.integers_32)
def test_basic(value: float, exponent: int) -> None:
    bound, ported = (BoundBigFloat(value, exponent),
                     PortedBigFloat(value, exponent))

    assert are_bound_ported_big_floats_equal(bound, ported)
