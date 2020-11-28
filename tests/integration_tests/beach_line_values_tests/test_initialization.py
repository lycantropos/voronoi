from hypothesis import given

from tests.bind_tests.hints import BoundBeachLineValue
from tests.integration_tests.hints import (BoundPortedMaybeCircleEventsPair,
                                           BoundPortedMaybeEdgesPair)
from tests.integration_tests.utils import (
    are_bound_ported_beach_line_values_equal)
from tests.port_tests.hints import PortedBeachLineValue
from . import strategies


@given(strategies.maybe_edges_pairs, strategies.maybe_circle_events_pairs)
def test_basic(maybe_edges_pair: BoundPortedMaybeEdgesPair,
               maybe_circle_events: BoundPortedMaybeCircleEventsPair) -> None:
    maybe_bound_edge, maybe_ported_edge = maybe_edges_pair
    maybe_bound_circle_event, maybe_ported_circle_event = maybe_circle_events
    bound, ported = (BoundBeachLineValue(maybe_bound_edge,
                                         maybe_bound_circle_event),
                     PortedBeachLineValue(maybe_ported_edge,
                                          maybe_ported_circle_event))

    assert are_bound_ported_beach_line_values_equal(bound, ported)
