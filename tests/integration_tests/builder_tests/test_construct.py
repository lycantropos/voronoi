from hypothesis import given

from tests.utils import (BoundPortedBuildersPair,
                         BoundPortedDiagramsPair,
                         are_bound_ported_builders_equal,
                         are_bound_ported_diagrams_equal,
                         equivalence)
from . import strategies


@given(strategies.valid_builders_pairs, strategies.empty_diagrams_pairs)
def test_basic(pair: BoundPortedBuildersPair,
               diagrams_pair: BoundPortedDiagramsPair) -> None:
    bound, ported = pair
    bound_diagram, ported_diagram = diagrams_pair

    bound_result = bound.construct(bound_diagram)
    ported_result = ported.construct(ported_diagram)

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_builders_equal(bound, ported)
    assert are_bound_ported_diagrams_equal(bound_diagram, ported_diagram)