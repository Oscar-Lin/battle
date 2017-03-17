from battle.maptools.direction import Direction

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Point({}, {})'.format(self._x, self._y)

    def in_direction(self, direction):
        directions = {N: (0, 1), S: (0, -1), E: (1, 0), W: (-1, 0)}
        del_x, del_y = directions[direction]
        return self.plus(del_x, del_y)

    def plus(self, x, y):
        return Point(self._x + x, self._y + y)

    def plus_x(self, x):
        return self.plus(x, 0)

    def plus_y(self, y):
        return self.plus(0, y)

    def at_distance(self, distance):
        if distance == 0:
            return [self]
        out = []
        for del_x in range(-distance, distance + 1):
            del_y = distance - abs(del_x)
            out.append(self.plus(del_x, del_y))
            if del_y != 0:
                out.append(self.plus(del_x, - del_y))
        return out


