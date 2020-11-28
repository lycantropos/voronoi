from hypothesis import given

from tests.port_tests.hints import PortedDiagram
from . import strategies


@given(strategies.diagrams)
def test_basic(diagram: PortedDiagram) -> None:
    result = diagram.clear()

    assert result is None
