from hypothesis import given

from tests.integration_tests.hints import BoundPortedBuildersWithDiagramsPair
from tests.integration_tests.utils import (are_bound_ported_builders_equal,
                                           are_bound_ported_diagrams_equal)
from tests.utils import equivalence
from . import strategies


@given(strategies.initialized_valid_builders_with_diagrams_pairs)
def test_basic(builders_with_diagrams_pair: BoundPortedBuildersWithDiagramsPair
               ) -> None:
    ((bound, bound_diagram),
     (ported, ported_diagram)) = builders_with_diagrams_pair

    bound_result = bound.init_beach_line(bound_diagram)
    ported_result = ported.init_beach_line(ported_diagram)

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_builders_equal(bound, ported)
    assert are_bound_ported_diagrams_equal(bound_diagram, ported_diagram)
