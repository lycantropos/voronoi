from hypothesis import given

from tests.bind_tests.hints import BoundDiagram
from . import strategies


@given(strategies.diagrams)
def test_basic(diagram: BoundDiagram) -> None:
    result = diagram.clear()

    assert result is None
