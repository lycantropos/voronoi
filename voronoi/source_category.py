from enum import (IntEnum,
                  unique)


@unique
class SourceCategory(IntEnum):
    # point subtypes
    SINGLE_POINT = 0x0
    SEGMENT_START_POINT = 0x1
    SEGMENT_END_POINT = 0x2

    # segment subtypes
    INITIAL_SEGMENT = 0x8
    REVERSE_SEGMENT = 0x9
