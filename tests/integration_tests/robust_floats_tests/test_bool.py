from hypothesis import given

from tests.utils import (BoundPortedRobustFloatsPair,
                         equivalence)
from . import strategies


@given(strategies.robust_floats_pairs)
def test_basic(pair: BoundPortedRobustFloatsPair) -> None:
    bound, ported = pair

    assert equivalence(bool(bound), bool(ported))
