from hypothesis import given

from tests.integration_tests.hints import BoundPortedSiteEventsPair
from tests.utils import equivalence
from . import strategies


@given(strategies.site_events_pairs)
def test_basic(pair: BoundPortedSiteEventsPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_segment, ported.is_segment)
