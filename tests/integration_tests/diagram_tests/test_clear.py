from hypothesis import given

from tests.integration_tests.hints import BoundPortedDiagramsPair
from tests.integration_tests.utils import are_bound_ported_diagrams_equal
from tests.utils import equivalence
from . import strategies


@given(strategies.diagrams_pairs)
def test_basic(pair: BoundPortedDiagramsPair) -> None:
    bound, ported = pair

    bound_result = bound.clear()
    ported_result = ported.clear()

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_diagrams_equal(bound, ported)
