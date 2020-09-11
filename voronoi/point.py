from reprit.base import generate_repr


class Point:
    __slots__ = 'x', 'y'

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    __repr__ = generate_repr(__init__)
