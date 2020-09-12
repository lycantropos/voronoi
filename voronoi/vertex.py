from reprit.base import generate_repr


class Vertex:
    __slots__ = 'x', 'y'

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Vertex') -> bool:
        return (self.x == other.x and self.y == other.y
                if isinstance(other, Vertex)
                else NotImplemented)
