from hypothesis import given

from tests.utils import (BoundPortedBuildersPair,
                         are_bound_ported_builders_equal,
                         equivalence)
from . import strategies


@given(strategies.builders_pairs)
def test_basic(pair: BoundPortedBuildersPair) -> None:
    bound, ported = pair

    assert equivalence(bound.init_sites_queue(),
                       ported.init_sites_queue())
    assert are_bound_ported_builders_equal(bound, ported)
