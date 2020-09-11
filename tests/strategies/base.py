from hypothesis import strategies

MAX_VALUE = 10 ** 6
MIN_VALUE = -MAX_VALUE
coordinates = strategies.integers(MIN_VALUE, MAX_VALUE)
integers_32 = strategies.integers(-2147483648, 2147483647)
