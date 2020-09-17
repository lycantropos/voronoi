from hypothesis import given

from tests.utils import (BoundPortedBeachLineKeysPair,
                         are_bound_ported_site_events_equal)
from . import strategies


@given(strategies.beach_line_keys_pairs)
def test_basic(pair: BoundPortedBeachLineKeysPair) -> None:
    bound, ported = pair

    assert are_bound_ported_site_events_equal(bound.comparison_site,
                                              ported.comparison_site)
