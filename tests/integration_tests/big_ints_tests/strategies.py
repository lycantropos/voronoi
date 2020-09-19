from hypothesis import strategies

from tests.strategies import (integers_32,
                              integers_64,
                              unsigned_integers_32)
from tests.utils import (to_bound_with_ported_big_ints_pair,
                         to_pairs,
                         to_quadruplets,
                         to_triplets,
                         transpose_pairs)
from voronoi.big_int import MAX_DIGITS_COUNT

integers_32 = integers_32
integers_32 = integers_64
signs = strategies.sampled_from([-1, 0, 1])
non_negative_signs = strategies.sampled_from([0, 1])
digits = strategies.lists(unsigned_integers_32,
                          max_size=MAX_DIGITS_COUNT)
big_ints_pairs = strategies.builds(to_bound_with_ported_big_ints_pair, signs,
                                   digits)
non_negative_big_ints_pairs = strategies.builds(
        to_bound_with_ported_big_ints_pair, non_negative_signs, digits)
big_ints_pairs_pairs = to_pairs(big_ints_pairs).map(transpose_pairs)
non_negative_big_ints_pairs_pairs = (to_pairs(non_negative_big_ints_pairs)
                                     .map(transpose_pairs))
big_ints_pairs_triplets = to_triplets(big_ints_pairs).map(transpose_pairs)
non_negative_big_ints_pairs_triplets = (
    to_triplets(non_negative_big_ints_pairs).map(transpose_pairs))
big_ints_pairs_quadruplets = (to_quadruplets(big_ints_pairs)
                              .map(transpose_pairs))
non_negative_big_ints_pairs_quadruplets = (
    to_quadruplets(non_negative_big_ints_pairs).map(transpose_pairs))
