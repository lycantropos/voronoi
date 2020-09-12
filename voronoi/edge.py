from reprit.base import generate_repr


class Edge:
    __slots__ = ('start_index', 'end_index', 'is_primary', 'is_linear',
                 'cell_index', 'twin_index')

    def __init__(self,
                 start_index: int,
                 end_index: int,
                 is_primary: bool,
                 is_linear: bool,
                 cell_index: int,
                 twin_index: int) -> None:
        self.start_index = start_index
        self.end_index = end_index
        self.is_primary = is_primary
        self.is_linear = is_linear
        self.cell_index = cell_index
        self.twin_index = twin_index

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Edge') -> bool:
        return (self.start_index == other.start_index
                and self.end_index == other.end_index
                and self.is_primary is other.is_primary
                and self.is_linear is other.is_linear
                and self.cell_index == other.cell_index
                and self.twin_index == other.twin_index
                if isinstance(other, Edge)
                else NotImplemented)
