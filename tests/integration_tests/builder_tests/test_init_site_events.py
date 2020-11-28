from hypothesis import given

from tests.integration_tests.hints import BoundPortedBuildersPair
from tests.integration_tests.utils import are_bound_ported_builders_equal
from tests.utils import equivalence
from . import strategies


@given(strategies.builders_pairs)
def test_basic(pair: BoundPortedBuildersPair) -> None:
    bound, ported = pair

    bound_result = bound.init_sites_queue()
    ported_result = ported.init_sites_queue()

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_builders_equal(bound, ported)
