from hypothesis import given

from tests.integration_tests.hints import BoundPortedVerticesPair
from tests.utils import equivalence
from . import strategies


@given(strategies.vertices_pairs)
def test_basic(pair: BoundPortedVerticesPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_degenerate, ported.is_degenerate)
