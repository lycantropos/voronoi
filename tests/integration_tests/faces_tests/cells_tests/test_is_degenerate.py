from hypothesis import given

from tests.integration_tests.hints import BoundPortedCellsPair
from tests.utils import equivalence
from . import strategies


@given(strategies.cells_pairs)
def test_basic(pair: BoundPortedCellsPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_degenerate, ported.is_degenerate)
