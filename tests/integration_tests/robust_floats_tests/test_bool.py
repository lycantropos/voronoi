from hypothesis import given

from tests.integration_tests.hints import BoundPortedRobustFloatsPair
from tests.utils import equivalence
from . import strategies


@given(strategies.robust_floats_pairs)
def test_basic(pair: BoundPortedRobustFloatsPair) -> None:
    bound, ported = pair

    assert equivalence(bool(bound), bool(ported))
