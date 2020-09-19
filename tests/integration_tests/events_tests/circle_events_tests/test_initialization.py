from hypothesis import given

from tests.utils import (BoundCircleEvent,
                         PortedCircleEvent,
                         are_bound_ported_circle_events_equal)
from . import strategies


@given(strategies.doubles, strategies.doubles, strategies.doubles,
       strategies.booleans)
def test_basic(center_x: float,
               center_y: float,
               lower_x: float,
               is_active: bool) -> None:
    bound, ported = (BoundCircleEvent(center_x, center_y, lower_x, is_active),
                     PortedCircleEvent(center_x, center_y, lower_x, is_active))

    assert are_bound_ported_circle_events_equal(bound, ported)
