from battle.maptools.direction import Direction
from typing import List, Any, Generator


N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class Point(object):
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __eq__(self, other: Any):
        if not isinstance(other, Point):
            return False
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other: Any):
        return not self == other

    def __lt__(self, other: 'Point'):
        return (self.y, self.x) < (other.y, other.x)

    def __le__(self, other: 'Point'):
        return self == other or self < other

    def __gt__(self, other: 'Point'):
        return not self <= other

    def __ge__(self, other: 'Point'):
        return not self < other

    def __repr__(self):
        return 'Point({}, {})'.format(self._x, self._y)

    def __str__(self):
        return '({}, {})'.format(self._x, self._y)

    def __hash__(self):
        return hash(repr(self))

    def in_direction(self, direction: Direction) -> 'Point':
        del_x, del_y = direction.value
        return self.plus(del_x, del_y)

    def plus(self, x: int, y: int) -> 'Point':
        return Point(self._x + x, self._y + y)

    def at_distance(self, distance: int) -> List['Point']:
        if distance == 0:
            return [self]
        out = []
        for del_x in range(-distance, distance + 1):
            del_y = distance - abs(del_x)
            out.append(self.plus(del_x, del_y))
            if del_y != 0:
                out.append(self.plus(del_x, - del_y))
        return sorted(out)

    def to_rectangle(self, x_size: int, y_size: int) -> List['Point']:
        out = []
        x_range = get_range(x_size)
        y_range = get_range(y_size)
        for del_x in x_range:
            for del_y in y_range:
                out.append(self.plus(del_x, del_y))
        return sorted(out)

    def generate_path(self, path: List[Direction]) -> Generator['Point', None, None]:

        def path_generator(start, path_):
            current = start
            for direction in path_:
                current = current.in_direction(direction)
                yield current

        return path_generator(self, path)


def get_range(stop_by):
    if stop_by < 0:
        return range(0, stop_by, -1)
    return range(stop_by)
