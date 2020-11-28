from typing import List

from hypothesis import given

from tests.bind_tests.hints import BoundBigInt
from tests.integration_tests.utils import are_bound_ported_big_ints_equal
from tests.port_tests.hints import PortedBigInt
from . import strategies


@given(strategies.signs, strategies.digits)
def test_basic(sign: int, digits: List[int]) -> None:
    bound, ported = BoundBigInt(sign, digits), PortedBigInt(sign, digits)

    assert are_bound_ported_big_ints_equal(bound, ported)
