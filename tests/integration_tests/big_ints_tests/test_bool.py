from hypothesis import given

from tests.utils import (BoundPortedBigIntsPair,
                         equivalence)
from . import strategies


@given(strategies.big_ints_pairs)
def test_basic(pair: BoundPortedBigIntsPair) -> None:
    bound, ported = pair

    assert equivalence(bool(bound), bool(ported))
