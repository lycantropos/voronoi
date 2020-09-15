from hypothesis import given

from tests.utils import (BoundPortedSiteEventsPair,
                         equivalence)
from . import strategies


@given(strategies.site_events_pairs, strategies.site_events_pairs)
def test_basic(first_pair: BoundPortedSiteEventsPair,
               second_pair: BoundPortedSiteEventsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
