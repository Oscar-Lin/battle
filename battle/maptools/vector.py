from battle.maptools.direction import Direction


class Vector(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @classmethod
    def from_dir_and_mag(cls, direction: Direction, magnitude: int):
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