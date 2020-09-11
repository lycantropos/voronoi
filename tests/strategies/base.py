from hypothesis import strategies

integers_32 = strategies.integers(-2 ** 31, 2 ** 31 - 1)
integers_64 = strategies.integers(-2 ** 63, 2 ** 63 - 1)
doubles = strategies.floats(allow_infinity=False,
                            allow_nan=False)
sizes = strategies.integers(0, 2 ** 32 - 1)
