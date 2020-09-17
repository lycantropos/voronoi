import sys
from decimal import Decimal

from hypothesis import strategies

integers_32 = strategies.integers(-2 ** 31, 2 ** 31 - 1)
integers_64 = strategies.integers(-2 ** 63, 2 ** 63 - 1)


def to_digits_count(number: float,
                    *,
                    max_digits_count: int = sys.float_info.dig) -> float:
    decimal = Decimal(number).normalize()
    _, significant_digits, exponent = decimal.as_tuple()
    significant_digits_count = len(significant_digits)
    if exponent < 0:
        fixed_digits_count = (1 - exponent
                              if exponent <= -significant_digits_count
                              else significant_digits_count)
    else:
        fixed_digits_count = exponent + significant_digits_count
    if fixed_digits_count <= max_digits_count:
        return number
    whole_digits_count = max(significant_digits_count + exponent, 0)
    if whole_digits_count:
        whole_digits_offset = max(whole_digits_count - max_digits_count, 0)
        decimal /= 10 ** whole_digits_offset
        whole_digits_count -= whole_digits_offset
    else:
        decimal *= 10 ** (-exponent - significant_digits_count)
        whole_digits_count = 1
    decimal = round(decimal, min(max(max_digits_count - whole_digits_count, 0),
                                 significant_digits_count))
    return float(str(decimal))


doubles = (strategies.floats(allow_infinity=False,
                             allow_nan=False)
           .map(to_digits_count))
sizes = strategies.integers(0, 2 ** 32 - 1)
