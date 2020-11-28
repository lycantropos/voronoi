from hypothesis import given

from tests.integration_tests.hints import BoundPortedBigIntsPair
from . import strategies


@given(strategies.big_ints_pairs)
def test_basic(pair: BoundPortedBigIntsPair) -> None:
    bound, ported = pair

    assert bound.frexp() == ported.frexp()
