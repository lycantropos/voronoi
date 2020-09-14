from reprit.base import generate_repr


class CircleEvent:
    __slots__ = 'center_x', 'center_y', 'lower_x', 'is_active'

    def __init__(self,
                 center_x: int,
                 center_y: int,
                 lower_x: int,
                 is_active: bool = True) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.lower_x = lower_x
        self.is_active = is_active

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'CircleEvent') -> bool:
        return (self.center_x == other.center_x
                and self.center_y == other.center_y
                and self.lower_x == other.lower_x
                and self.is_active is other.is_active
                if isinstance(other, CircleEvent)
                else NotImplemented)

    @property
    def lower_y(self) -> int:
        return self.center_y

    @property
    def x(self) -> int:
        return self.center_x

    @x.setter
    def x(self, value: int) -> None:
        self.center_x = value

    @property
    def y(self) -> int:
        return self.center_y

    @y.setter
    def y(self, value: int) -> None:
        self.center_y = value

    def deactivate(self) -> 'CircleEvent':
        self.is_active = False
        return self
