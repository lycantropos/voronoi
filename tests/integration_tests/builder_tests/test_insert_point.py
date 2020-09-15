from hypothesis import given

from tests.utils import (BoundPortedBuildersPair,
                         are_bound_ported_builders_equal)
from . import strategies


@given(strategies.builders_pairs, strategies.coordinates,
       strategies.coordinates)
def test_basic(pair: BoundPortedBuildersPair, x: int, y: int) -> None:
    bound, ported = pair

    assert bound.insert_point(x, y) == ported.insert_point(x, y)
    assert are_bound_ported_builders_equal(bound, ported)
