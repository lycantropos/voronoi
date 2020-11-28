from hypothesis import given

from tests.port_tests.hints import (PortedDiagram,
                                    PortedPointsList,
                                    PortedSegmentsList)
from . import strategies


@given(strategies.empty_diagrams, strategies.multipoints)
def test_multipoints(diagram: PortedDiagram,
                     multipoint: PortedPointsList) -> None:
    result = diagram.construct(multipoint, [])

    assert result is None


@given(strategies.empty_diagrams, strategies.multisegments)
def test_multisegments(diagram: PortedDiagram,
                       multisegment: PortedSegmentsList) -> None:
    result = diagram.construct([], multisegment)

    assert result is None
