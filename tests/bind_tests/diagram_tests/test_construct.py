from hypothesis import given

from tests.bind_tests.hints import (BoundDiagram,
                                    BoundPointsList,
                                    BoundSegmentsList)
from . import strategies


@given(strategies.empty_diagrams, strategies.multipoints)
def test_multipoints(diagram: BoundDiagram,
                     multipoint: BoundPointsList) -> None:
    try:
        result = diagram.construct(multipoint, [])
    except ValueError:
        pass
    else:
        assert result is None


@given(strategies.empty_diagrams, strategies.multisegments)
def test_multisegments(diagram: BoundDiagram,
                       multisegment: BoundSegmentsList) -> None:
    try:
        result = diagram.construct([], multisegment)
    except ValueError:
        pass
    else:
        assert result is None
