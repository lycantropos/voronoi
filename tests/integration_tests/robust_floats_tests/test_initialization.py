from hypothesis import given

from tests.bind_tests.hints import BoundRobustFloat
from tests.integration_tests.utils import are_bound_ported_robust_floats_equal
from tests.port_tests.hints import PortedRobustFloat
from . import strategies


@given(strategies.doubles, strategies.doubles)
def test_basic(value: float, relative_error: float) -> None:
    bound, ported = (BoundRobustFloat(value, relative_error),
                     PortedRobustFloat(value, relative_error))

    assert are_bound_ported_robust_floats_equal(bound, ported)
