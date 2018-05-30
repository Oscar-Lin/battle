from enum import Enum
from functools import reduce
from math import sqrt


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


class CompositeDirection(object):
    def __init__(self, *directions: Direction):
        self._name = reduce(lambda acc, el: acc + el.name, directions, '')
        value_iterator = (el.value for el in directions)
        total_x, total_y = (sum(el) for el in zip(*value_iterator))
        magnitude = sqrt(total_x**2 + total_y**2)
        if magnitude == 0:
            raise ValueError('CompositeDirection may not be zero values. i.e. N+S is not allowed.')
        self._x = total_x/magnitude
        self._y = total_y/magnitude
        self._directions = tuple(directions)

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._x, self._y

    def __str__(self):
        return self._name

    def __repr__(self):
        return 'CompositeDirection{!r}'.format(self._directions)

    def __eq__(self, other):
        if not isinstance(other, CompositeDirection):
            return False
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def opposite(self) -> 'CompositeDirection':
        opposites = [direction.opposite() for direction in self._directions]
        return CompositeDirection(*opposites)

    def left(self) -> 'CompositeDirection':
        lefts = [direction.left() for direction in self._directions]
        return CompositeDirection(*lefts)

    def right(self) -> 'CompositeDirection':
        rights = [direction.right() for direction in self._directions]
        return CompositeDirection(*rights)
