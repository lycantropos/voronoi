from hypothesis import given

from tests.port_tests.hints import (PortedDiagram,
                                    PortedPointsList,
                                    PortedSegmentsList)
from . import strategies


@given(strategies.empty_diagrams, strategies.multipoints)
def test_multipoints(diagram: PortedDiagram,
                     multipoint: PortedPointsList) -> None:
    try:
        result = diagram.construct(multipoint, [])
    except ValueError:
        pass
    else:
        assert result is None


@given(strategies.empty_diagrams, strategies.multisegments)
def test_multisegments(diagram: PortedDiagram,
                       multisegment: PortedSegmentsList) -> None:
    try:
        result = diagram.construct([], multisegment)
    except ValueError:
        pass
    else:
        assert result is None
