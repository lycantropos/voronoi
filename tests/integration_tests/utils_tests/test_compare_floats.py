from _voronoi import compare_floats as bound
from hypothesis import given

from voronoi.utils import compare_floats as ported
from . import strategies


@given(strategies.floats, strategies.floats, strategies.sizes)
def test_basic(left: float, right: float, max_ulps: int) -> None:
    assert bound(left, right, max_ulps) == ported(left, right, max_ulps)
