from hypothesis import given

from tests.utils import (BoundPortedEventsPair,
                         equivalence)
from . import strategies


@given(strategies.events_pairs, strategies.events_pairs)
def test_basic(first_pair: BoundPortedEventsPair,
               second_pair: BoundPortedEventsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound < second_bound,
                       first_ported < second_ported)
