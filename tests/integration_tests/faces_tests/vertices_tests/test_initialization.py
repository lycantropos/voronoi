from hypothesis import given

from tests.bind_tests.hints import BoundVertex
from tests.integration_tests.utils import are_bound_ported_vertices_equal
from tests.port_tests.hints import PortedVertex
from . import strategies


@given(strategies.coordinates, strategies.coordinates)
def test_basic(x: int, y: int) -> None:
    bound, ported = BoundVertex(x, y), PortedVertex(x, y)

    assert are_bound_ported_vertices_equal(bound, ported)
