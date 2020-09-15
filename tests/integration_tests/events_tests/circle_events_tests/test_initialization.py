from hypothesis import given

from tests.utils import (BoundCircleEvent,
                         PortedCircleEvent,
                         are_bound_ported_circle_events_equal)
from . import strategies


@given(strategies.coordinates, strategies.coordinates, strategies.coordinates,
       strategies.booleans)
def test_basic(center_x: int,
               center_y: int,
               lower_x: int,
               is_active: bool) -> None:
    bound, ported = (BoundCircleEvent(center_x, center_y, lower_x, is_active),
                     PortedCircleEvent(center_x, center_y, lower_x, is_active))

    assert are_bound_ported_circle_events_equal(bound, ported)
