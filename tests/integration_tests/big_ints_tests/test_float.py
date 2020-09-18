from hypothesis import given

from tests.utils import BoundPortedBigIntsPair
from . import strategies


@given(strategies.big_ints_pairs)
def test_basic(pair: BoundPortedBigIntsPair) -> None:
    bound, ported = pair

    assert float(bound) == float(ported)
