from hypothesis import given

from tests.integration_tests.hints import BoundPortedBeachLineKeysPair
from . import strategies


@given(strategies.beach_line_keys_pairs, strategies.booleans)
def test_basic(pair: BoundPortedBeachLineKeysPair, is_new_node: bool) -> None:
    bound, ported = pair

    assert (bound.to_comparison_y(is_new_node)
            == ported.to_comparison_y(is_new_node))
