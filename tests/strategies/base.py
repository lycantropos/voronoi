from hypothesis import strategies

integers_32 = strategies.integers(-2147483648, 2147483647)
doubles = strategies.floats(allow_infinity=False,
                            allow_nan=False)
