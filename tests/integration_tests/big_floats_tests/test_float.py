from hypothesis import given

from tests.integration_tests.hints import BoundPortedBigFloatsPair
from . import strategies


@given(strategies.big_floats_pairs)
def test_basic(pair: BoundPortedBigFloatsPair) -> None:
    bound, ported = pair

    assert float(bound) == float(ported)
