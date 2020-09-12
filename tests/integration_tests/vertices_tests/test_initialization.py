from hypothesis import given

from tests.utils import (BoundVertex,
                         PortedVertex,
                         are_bound_ported_vertices_equal)
from . import strategies


@given(strategies.doubles, strategies.doubles)
def test_basic(x: int, y: int) -> None:
    bound, ported = BoundVertex(x, y), PortedVertex(x, y)

    assert are_bound_ported_vertices_equal(bound, ported)
