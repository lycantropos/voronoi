import struct
from enum import (IntEnum,
                  unique)


@unique
class ComparisonResult(IntEnum):
    LESS = -1
    EQUAL = 0
    MORE = 1


def compare_floats(left: float, right: float, max_ulps: int
                   ) -> ComparisonResult:
    left_uint, right_uint = _float_to_uint(left), _float_to_uint(right)
    return ((ComparisonResult.EQUAL
             if left_uint - right_uint <= max_ulps
             else ComparisonResult.LESS)
            if left_uint > right_uint
            else (ComparisonResult.EQUAL
                  if right_uint - left_uint <= max_ulps
                  else ComparisonResult.MORE))


def _float_to_uint(value: float,
                   *,
                   sign_bit_mask: int = 2 ** 63) -> int:
    result = int.from_bytes(struct.pack('!d', value), 'big')
    return sign_bit_mask - result if result < sign_bit_mask else result
