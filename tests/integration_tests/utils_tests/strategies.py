from hypothesis import strategies

from tests.strategies import (integers_32,
                              sizes)

coordinates = integers_32
sizes = sizes
floats = strategies.floats(allow_nan=False,
                           allow_infinity=False)
