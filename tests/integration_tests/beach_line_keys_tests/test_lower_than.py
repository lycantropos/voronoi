from hypothesis import given

from tests.integration_tests.hints import BoundPortedBeachLineKeysPair
from tests.utils import equivalence
from . import strategies


@given(strategies.beach_line_keys_pairs, strategies.beach_line_keys_pairs)
def test_basic(first_pair: BoundPortedBeachLineKeysPair,
               second_pair: BoundPortedBeachLineKeysPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound < second_bound,
                       first_ported < second_ported)
