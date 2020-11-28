from enum import Enum
from operator import is_
from typing import (Callable,
                    List,
                    Optional,
                    Sequence,
                    Tuple,
                    Type,
                    TypeVar)

from hypothesis import strategies
from hypothesis.strategies import SearchStrategy
from hypothesis_geometry.hints import (Multipoint as RawMultipoint,
                                       Multisegment as RawMultisegment)

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy
RawMultipoint = RawMultipoint
RawMultisegment = RawMultisegment


def enum_to_values(cls: Type[Enum]) -> List[Enum]:
    return [value for _, value in sorted(cls.__members__.items())]


equivalence = is_


def transpose_pairs(pairs: List[Tuple[Domain, Range]]
                    ) -> Tuple[List[Domain], List[Range]]:
    return tuple(map(list, zip(*pairs))) if pairs else ([], [])


def to_maybe_equals(equals: Callable[[Domain, Range], bool]
                    ) -> Callable[[Optional[Domain], Optional[Range]], bool]:
    def maybe_equals(left: Optional[Domain], right: Optional[Range]) -> bool:
        return ((left is None) is (right is None)
                and (left is None or equals(left, right)))

    return maybe_equals


def to_sequences_equals(equals: Callable[[Domain, Range], bool]
                        ) -> Callable[[Sequence[Domain], Sequence[Range]],
                                      bool]:
    def sequences_equals(left: Sequence[Domain],
                         right: Sequence[Range]) -> bool:
        return len(left) == len(right) and all(map(equals, left, right))

    return sequences_equals


def to_maybe(strategy: Strategy[Domain]) -> Strategy[Optional[Domain]]:
    return strategies.none() | strategy


def to_maybe_pairs(strategy: Strategy[Tuple[Domain, Range]]
                   ) -> Strategy[Tuple[Optional[Domain], Optional[Range]]]:
    return to_pairs(strategies.none()) | strategy


def to_pairs(strategy: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(strategy, strategy)


def to_quadruplets(strategy: Strategy[Domain]
                   ) -> Strategy[Tuple[Domain, Domain, Domain, Domain]]:
    return strategies.tuples(strategy, strategy, strategy, strategy)


def to_triplets(strategy: Strategy[Domain]
                ) -> Strategy[Tuple[Domain, Domain, Domain]]:
    return strategies.tuples(strategy, strategy, strategy)
