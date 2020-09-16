from hypothesis import given

from tests.utils import (BoundPortedDiagramsPair,
                         BoundPortedSiteEventsPair,
                         equivalence)
from . import strategies


@given(strategies.diagrams_pairs, strategies.site_events_pairs,
       strategies.site_events_pairs)
def test_basic(pair: BoundPortedDiagramsPair,
               first_events_pair: BoundPortedSiteEventsPair,
               second_events_pair: BoundPortedSiteEventsPair) -> None:
    bound, ported = pair
    bound_first_event, ported_first_event = first_events_pair
    bound_second_event, ported_second_event = second_events_pair

    assert equivalence(bound.is_linear_edge(bound_first_event,
                                            bound_second_event),
                       ported.is_linear_edge(ported_first_event,
                                             ported_second_event))
