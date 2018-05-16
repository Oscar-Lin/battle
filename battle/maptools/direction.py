from enum import Enum


class Direction(Enum):
    N = (0, 1)
    S = (0, -1)
    E = (1, 0)
    W = (-1, 0)

    def opposite(self) -> 'Direction':
        opposites = {self.N: self.S, self.S: self.N, self.E: self.W, self.W: self.E}
        return opposites[self]

    def left(self) -> 'Direction':
        lefts = {self.N: self.W, self.W: self.S, self.S: self.E, self.E: self.N}
        return lefts[self]

    def right(self) -> 'Direction':
        rights = {self.N: self.E, self.E: self.S, self.S: self.W, self.W: self.N}
        return rights[self]

    def __repr__(self):
        return 'Direction.{}'.format(self.name)

    def __lt__(self, other: 'Direction'):
        return (self.value[1], self.value[0]) < (other.value[1], other.value[0])

    def __le__(self, other: 'Direction'):
        return self < other or self == other

    def __gt__(self, other: 'Direction'):
        return not self <= other

    def __ge__(self, other: 'Direction'):
        return not self < other

