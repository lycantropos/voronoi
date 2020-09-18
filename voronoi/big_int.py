import ctypes
from typing import List

from reprit.base import generate_repr

from voronoi.utils import to_sign

MAX_DIGITS_COUNT = 64


def _to_uint32(value: int) -> int:
    return ctypes.c_uint32(value).value


class BigInt:
    __slots__ = 'digits', 'sign'

    def __init__(self, digits: List[int], sign: int) -> None:
        if not (sign and digits):
            sign, digits = 0, []
        self.digits = digits
        self.sign = sign if digits else 0

    __repr__ = generate_repr(__init__)

    def __bool__(self) -> bool:
        return bool(self.sign)

    def __add__(self, other: 'BigInt') -> 'BigInt':
        result = BigInt([], 0)
        result._add(self, other)
        return result

    def __neg__(self) -> 'BigInt':
        return BigInt(self.digits[:], -self.sign)

    def __sub__(self, other: 'BigInt') -> 'BigInt':
        result = BigInt([], 0)
        result._subtract(self, other)
        return result

    def _add(self, left: 'BigInt', right: 'BigInt') -> None:
        if not left.sign:
            self.sign, self.digits = right.sign, right.digits[:]
            return
        elif not right.sign:
            self.sign, self.digits = left.sign, left.digits[:]
            return
        elif (left.sign > 0) is (left.sign > 0):
            self._add_digits(left.digits, right.digits)
        else:
            self._subtract_digits(left.digits, len(left.digits), right.digits,
                                  len(right.digits))
        if left.sign < 0:
            self.sign = -self.sign

    def _add_digits(self,
                    left_digits: List[int],
                    right_digits: List[int]) -> None:
        left_size, right_size = len(left_digits), len(right_digits)
        if left_size < right_size:
            self._add_digits(right_digits, left_digits)
            return
        self.sign = to_sign(left_size)
        cursor = 0
        for index, right_digit in enumerate(right_digits):
            cursor += left_digits[index] + right_digit
            self.digits.append(_to_uint32(cursor))
            cursor >>= 32
        for index in range(right_size, left_size):
            cursor += left_digits[index]
            self.digits.append(cursor)
            cursor >>= 32
        if cursor and len(self.digits) < MAX_DIGITS_COUNT:
            self.digits.append(cursor)

    def _subtract(self, e1: 'BigInt', e2: 'BigInt') -> None:
        if not e1.sign:
            self.sign, self.digits = -e2.sign, e2.digits[:]
            return
        elif not e2.sign:
            self.sign, self.digits = e1.sign, e1.digits[:]
            return
        elif (e1.sign > 0) is (e2.sign > 0):
            self._subtract_digits(e1.digits, len(e1.digits), e2.digits,
                                  len(e2.digits))
        else:
            self._add_digits(e1.digits, e2.digits)
        if e1.sign < 0:
            self.sign = -self.sign

    def _subtract_digits(self,
                         left_digits: List[int],
                         left_limit: int,
                         right_digits: List[int],
                         right_limit: int,
                         is_recursive_call: bool = False) -> None:
        if left_limit < right_limit:
            self._subtract_digits(right_digits, right_limit, left_digits,
                                  left_limit, True)
            self.sign = -self.sign
            return
        elif not is_recursive_call and left_limit == right_limit:
            left_limit = left_limit
            while True:
                left_limit -= 1
                if left_digits[left_limit] < right_digits[left_limit]:
                    left_limit += 1
                    self._subtract_digits(right_digits, left_limit,
                                          left_digits,
                                          left_limit, True)
                    self.sign = -self.sign
                    return
                elif left_digits[left_limit] > right_digits[left_limit]:
                    left_limit += 1
                    break
                elif not left_limit:
                    break
            if not left_limit:
                self.sign = 0
                return
            right_limit = left_limit
        self.sign = to_sign(left_limit - 1)
        flag = False
        for index in range(right_limit):
            self.digits.append(_to_uint32(left_digits[index]
                                          - right_digits[index] - flag))
            flag = (left_digits[index] < right_digits[index]
                    or left_digits[index] == right_digits[index] and flag)
        for index in range(right_limit, left_limit):
            self.digits.append(_to_uint32(left_digits[index] - flag))
            flag = not left_digits[index] and flag
        if self.digits[-1]:
            self.sign = 1
        else:
            self.digits.pop()