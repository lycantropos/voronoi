from hypothesis import given

from tests.utils import (BoundPortedSiteEventsPair,
                         equivalence)
from . import strategies


@given(strategies.site_events_pairs)
def test_basic(pair: BoundPortedSiteEventsPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_point, ported.is_point)
