from hypothesis import strategies

from tests.strategies import sizes

sizes = sizes
floats = strategies.floats(allow_nan=False,
                           allow_infinity=False)
