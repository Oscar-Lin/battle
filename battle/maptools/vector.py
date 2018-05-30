from typing import Union, Tuple
from math import sqrt

from battle.maptools.direction import Direction, CompositeDirection


class Vector(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @classmethod
    def from_dir_and_mag(cls, direction: Union[Direction, CompositeDirection], magnitude: int):
        base_x, base_y = direction.value
        return cls(base_x * magnitude, base_y * magnitude)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def direction_tuple(self):
        x_dir = Direction.E
        x_val = abs(self.x)
        if self.x < 0:
            x_dir = x_dir.opposite()

        y_dir = Direction.N
        y_val = abs(self.y)
        if self.y < 0:
            y_dir = y_dir.opposite()

        return (x_dir, x_val), (y_dir, y_val)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    def to_dir_and_mag(self) -> Tuple[CompositeDirection, float]: # TODO test
        if self == Vector(0, 0):
            return CompositeDirection(Direction.N), 0.0

        if self.x > 0:
            x_dir = Direction.E
        else:
            x_dir = Direction.W
        if self.y > 0:
            y_dir = Direction.N
        else:
            y_dir = Direction.S
        total_dir = abs(self.x)*[x_dir] + abs(self.y)*[y_dir]
        direction = CompositeDirection(*total_dir)
        magnitude = sqrt(self.x**2 + self.y**2)
        return direction, magnitude


class DangerOpportunity(object):
    def __init__(self, danger: Vector, opportunity: Vector):
        self._danger = danger
        self._opportunity = opportunity

    @property
    def danger(self):
        return self._danger

    @property
    def opportunity(self):
        return self._opportunity

    def add(self, other: 'DangerOpportunity'):
        new_danger = self.danger.add(other.danger)
        new_opportunity = self.opportunity.add(other.opportunity)
        return DangerOpportunity(new_danger, new_opportunity)

    @classmethod
    def empty(cls):
        return DangerOpportunity(Vector(0, 0), Vector(0, 0))

    def __eq__(self, other):
        if not isinstance(other, DangerOpportunity):
            return False
        return (self.danger, self.opportunity) == (other.danger, other.opportunity)